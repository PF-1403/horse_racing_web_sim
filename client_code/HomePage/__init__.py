from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.server
import anvil.js
import random
import copy

class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.participant_id = anvil.server.call('get_or_make_id')
    self.initialise_app()
    self.race_started = False
    # Any code you write here will run before the form opens.
    self.place_bet_1.set_event_handler("x-place-bet", self.handle_place_bet)
    self.race_canvas_1.set_event_handler("x-start-race", self.start_race)
    anvil.js.window.setTimeout(self.walkthrough, 100)

  def initialise_app(self):
    self.balance = 1000.0
    self.race_index = 0
    self.finish_line = 100
    self.race_started = False
    self.race_winner = None
    self.bets_closed = False
    self.backed_horse = None
    self.race_ids = ["race1", "race2", "race3", "race4", "race5"]
    fixed = self.race_ids[0]
    shuffle = self.race_ids[1:]
    random.shuffle(shuffle)
    self.race_ids = [fixed] + shuffle
    print("Initialisation of app is complete!")

    self.load_next_race()

  def load_next_race(self):
    anvil.server.call('clear_bets_table')
    race_id = self.race_ids[self.race_index]
    self.race_spec = anvil.server.call('get_race_spec',race_id)
    print(f'Race Loaded! \nRace number {self.race_index+1}/{len(self.race_ids)}')
    print(f'Race spec: {self.race_spec["config_id"]}')

    self.race_canvas_1.reset_button()
    self.place_bet_1.bet_button.enabled = True
    self.odds_table_1.populate_static_odds(self.race_spec['competitors'])
    self.balance_bar_1.update_info(balance=self.balance, race_number=self.race_index+1, total_races=len(self.race_ids))

  def update_balance_bar(self):
    self.balance_bar_1.update_info(balance=self.balance, race_number=self.race_index + 1, total_races=len(self.race_ids))

  def update_stakes(self):
    stake, winnings = anvil.server.call('sum_logs')
    self.odds_table_1.update_stakes(stake, winnings)
  
  def calculate_dynamic_odds(self, competitors, positions):
    leader_position = max(horse['x'] for horse in positions)
    leader_progress = float(leader_position) / float(self.finish_line)
    odds = {}

    for comp in competitors:
      # Calculate relative positions
      current_position = next((value['x'] for value in positions if value['id'] == comp['id']), None)
      progress = float(current_position) / float(self.finish_line)
      relative_progress = progress / leader_progress

      # Do adaptions based upon closeness
      if leader_position - current_position == 0:
        win_probability = 1
      elif abs(leader_position - current_position) <= 0.1:
        win_probability = 0.5 * relative_progress
      else:
        win_probability = 0.3 * relative_progress

      # Calculate final odds
      dynamic_odds = max(1.01, (1 / win_probability))

      # Add odds to dict
      odds[comp["id"]] = dynamic_odds

    # Populate the odds table with the new odds
    self.odds_table_1.populate_dynamic_odds(odds)
  
  def handle_place_bet(self, **event_args):
    comp_id = event_args['comp_id']
    bet_amt = event_args['bet_amt']

    if bet_amt > self.balance:
      Notification("Insufficient funds!", style="warning").show()
      return

    valid_comp = next((comp for comp in self.race_spec['competitors'] if comp['id'] == comp_id), None)
    if not valid_comp:
      Notification("Invalid competitor ID entered!", style="warning").show()
      return

    if not self.race_started:
      static_odds = next((c["initial_odds"] for c in self.race_spec["competitors"] if c["id"] == comp_id), None)
      self.balance, bet_log = anvil.server.call('place_bet', comp_id, bet_amt, static_odds, self.balance, self.race_spec['config_id'])
      Notification(f"Bet placed on horse {comp_id} for £{bet_amt:.2f} at odds of {static_odds:.2f}", style="success").show()
      self.backed_horse = comp_id
      print("Successfully placed static bet")
    else:
      dynamic_odds = self.odds_table_1.get_current_odds(comp_id)
      self.balance, bet_log = anvil.server.call('place_bet', comp_id, bet_amt, dynamic_odds, self.balance, self.race_spec['config_id'])
      Notification(f"Bet placed on horse {comp_id} for £{bet_amt:.2f} at odds of {dynamic_odds:.2f}", style="success").show()
      print("Successfully placed dynamic bet")

    self.update_stakes()
    self.update_balance_bar()

  def start_race(self, **event_args):
    # Establish initial horse location, show race started
    bet_placed = self.check_pre_bet()
    if not bet_placed:
      self.race_canvas_1.button_1.enabled = True
      return
    self.horse_location = event_args['horses']
    self.finish_line = event_args['finish_line']
    self.race_started = True 
    self.race_timer.enabled = True
    self.bets_closed = False
    self.race_log = {}
    self.favourite = self.race_spec['favourite_id']
    self.second = self.race_spec['second_id']
    self.third = self.race_spec['third_id']
    if self.favourite == self.backed_horse:
      self.favourite = self.race_spec['second_id']
    self.fallen_ids = set()

  def check_pre_bet(self):
    if not self.backed_horse:
      Notification("You must place a pre-race bet!", style="danger").show()
      return False
    else:
      return True
  
  def race_timer_tick(self, **event_args):
    if not self.race_started:
      return

    race_ongoing = False
    for horse in self.horse_location:
      if horse['id'] in getattr(self, 'fallen_ids', set()):
        continue 
      # Check which race is being called
      if horse['x'] < self.finish_line:
        if self.race_spec['config_id'] == 'race1':
            horse['x'] = min(horse['x'] + random.randint(1, 5), self.finish_line)
            race_ongoing = True
          
        elif self.race_spec['config_id'] == 'race2':
          if horse['id'] == self.race_spec['favourite_id']:
            horse['x'] = min(horse['x'] + (1.2 * random.randint(1, 5)), self.finish_line)
            print(f'Horse {horse["id"]} boosted!')
          else:
            horse['x'] = min(horse['x'] + random.randint(1, 5), self.finish_line)
          race_ongoing = True
          
        elif self.race_spec['config_id'] == 'race3':
          if horse['id'] == self.backed_horse:
            if horse['x'] < 0.3 * self.finish_line:
              horse['x'] = horse['x'] + random.randint(1, 5)
            elif (horse['x'] > (0.3 * self.finish_line)) and (horse['x'] < (0.7 * self.finish_line)):
              horse['x'] = horse['x'] + (1.25 * random.randint(1, 5))
            else:
              horse['x'] = min(horse['x'] + (0.65 * random.randint(1, 5)), self.finish_line)
          else:
            horse['x'] = min(horse['x'] + random.randint(1, 5), self.finish_line)
          race_ongoing = True
          
        elif self.race_spec['config_id'] == 'race4':
          if horse['id'] == self.backed_horse:
            if horse['x'] < 0.2 * self.finish_line:
              horse['x'] = horse['x'] + (0.6 * random.randint(1, 5))
            elif (horse['x'] > (0.2 * self.finish_line)) and (horse['x'] < (0.7 * self.finish_line)):
              horse['x'] = horse['x'] + (1.2 * random.randint(1, 5))
            else:
              horse['x'] = min(horse['x'] + (1.3 * random.randint(1, 5)), self.finish_line)
          elif horse['id'] == self.favourite:
            if horse['x'] < 0.2 * self.finish_line:
              horse['x'] = horse['x'] + (0.6 * random.randint(1, 5))
            elif (horse['x'] > (0.2 * self.finish_line)) and (horse['x'] < (0.7 * self.finish_line)):
              horse['x'] = horse['x'] + (1.4 * random.randint(1, 5))
            else:
              horse['x'] = min(horse['x'] + (1.1 * random.randint(1, 5)), self.finish_line)        
          else:
            horse['x'] = min(horse['x'] + random.randint(1, 5), self.finish_line)
          race_ongoing = True

        elif self.race_spec['config_id'] == 'race5':
          if horse['id'] == self.favourite:
            if horse['id'] in self.fallen_ids:
              continue  # Already fallen, stays still, not race_ongoing
            if horse['x'] < 0.5 * self.finish_line:
              horse['x'] = horse['x'] + random.randint(1, 5)
              race_ongoing = True
            else:
              print("Horse has fallen")
              self.fallen_ids.add(horse['id'])  # Mark as fallen
              Notification(f"Horse {horse['id']} has fallen!", style="danger", timeout=0.75).show()
              # Do not set race_ongoing
              continue
          elif horse['id'] == self.second:
            if horse['x'] < 0.5 * self.finish_line:
              horse['x'] = horse['x'] + random.randint(1, 5)
            else:
              horse['x'] = min(horse['x'] + (0.9 * random.randint(1, 5)), self.finish_line)        
          elif horse['id'] == self.third:
            if horse['x'] < 0.5 * self.finish_line:
              horse['x'] = horse['x'] + random.randint(1, 5)
            else:
              horse['x'] = min(horse['x'] + (1.1 * random.randint(1, 5)), self.finish_line)           
          else:
            horse['x'] = min(horse['x'] + (0.8 * random.randint(1, 5)), self.finish_line)
          race_ongoing = True

    # Add location to race_log
    timestamp = str(datetime.utcnow().timestamp())
    self.race_log[timestamp] = copy.deepcopy(self.horse_location)  

    # Check for bets closed
    if not self.bets_closed:
      for horse in self.horse_location:        
        if (horse['x'] >= (0.8 * self.finish_line)):
          self.bets_closed = True
          Notification("No More Bets!", style="danger", timeout=0.75).show()
          self.place_bet_1.bet_button.enabled = False
          break
  
    # Check for race winner
    if self.race_winner is None:
      for horse in self.horse_location:        
          # Check for race winner
          if (horse['x'] == self.finish_line):
            self.race_winner = horse['id']
            break
          
    self.race_canvas_1.draw_canvas(self.horse_location)
    
    ## Now populate dynamic odds here ##
    self.calculate_dynamic_odds(self.race_spec['competitors'], self.horse_location)
    
    if not race_ongoing:
      self.race_timer.enabled = False
      self.race_started = False
      self.backed_horse = None
      self.race_complete()

  def calc_and_disp_results(self):
    stake, winnings = anvil.server.call('sum_logs')
    print(f'Race winner: {self.race_winner}')
    lost_stake = 0
    total_winnings = 0
    stake_returned = 0
    
    for id, amount in stake.items():
      if int(id) != int(self.race_winner):
        lost_stake += float(amount)
      elif int(id) == int(self.race_winner):
        self.balance += amount
        stake_returned = amount
                
    for id, value in winnings.items():
      if int(id) == int(self.race_winner):
        total_winnings = float(value)

    if total_winnings > 0:
      self.balance += total_winnings
      self.update_balance_bar()

    self.race_index += 1
    if self.race_index == len(self.race_ids):
      self.display_results_end(lost_stake, total_winnings, stake_returned)
    else:
      self.display_results_next_race(lost_stake, total_winnings, stake_returned)

    
  def display_results_next_race(self, stake, winnings, stake_returned):
    next_race = alert(
      title=f'Race Complete - Horse {self.race_winner} Won!',
      content=(
        f"Stakes lost on losers:                     £{stake:.2f}\n"
        f"Amount won on winners:               £{winnings:.2f}\n"
        f"Stakes returned:                              £{stake_returned:.2f}\n"
        f"\n"
        f"New balance:                                   £{self.balance:.2f}"
      ),
      buttons=[("Next Race", True)],
      dismissible=False,
      large=True
    )
  
    if next_race:
      if self.race_index == 1:
        self.balance = 1000
        Notification("Balance reset! Starting simulation.", style="info").show()
      self.race_winner = None
      self.race_canvas_1.reset_canvas()
      self.load_next_race()
      
  def display_results_end(self, stake, winnings, stake_returned):
    end_page = alert(
      title=f'Final Race Complete - Horse {self.race_winner} Won! \nThanks For Participating!',
      content=(
        f"Stakes lost on losers:                     £{stake:.2f}\n"
        f"Amount won on winners:               £{winnings:.2f}\n"
        f"Stakes returned:                              £{stake_returned:.2f}\n"
        f"\n"
        f"New balance:                                   £{self.balance:.2f}"
      ),
      buttons=[("Complete", True)],
      dismissible=False,
      large=True
    )

    if end_page:
      anvil.server.call('clear_bets_table')
      open_form('EndForm')

  def log_results(self):
    with anvil.server.no_loading_indicator:
      anvil.server.call('launch_background_tasks', self.race_log, self.race_spec['config_id'])

  def race_complete(self):
    self.log_results()
    self.calc_and_disp_results()
    
  def walkthrough(self):
    self.balance_bar_1.role = "highlighted"
    alert("      This is the Balance Bar.\n\n"
          "It displays your total balance and race progress.", 
          title="Walkthrough")
    self.balance_bar_1.role = None
    
    self.odds_table_1.role = "highlighted"
    alert("  This is the Odds Table. \n\n"
          "The odds for each horse are shown here, alongside the total amount" 
          " staked and potential winnings for each horse in the race.\n\n"
          "Odds are decimal, with lower odds meaning a higher likelihood of winning.", 
          title="Walkthrough")
    self.odds_table_1.role = None

    self.place_bet_1.role = "highlighted"
    alert("  This is the Place Bets Widget. \n\n"
          "Enter the ID (1-4) of the horse you want to bet on and the stake amount. \n\n" 
          "A pre-race bet must be placed for each race, and you can bet freely in-race\n\n"
          "You can press the 'Place Bet' button or the enter key once information has been entered.", 
          title="Walkthrough")
    self.place_bet_1.role = None

    self.race_canvas_1.role = "highlighted"
    alert("      This is the Race Canvas. \n"
          "This displays the progress of each horse in the race. \n\n" 
          "Bets can't be placed past the dashed line showing 80% race distance.\n\n"
          "Once you have placed your pre-race bet, click 'Start Race' to begin.", 
          title="Walkthrough")
    self.race_canvas_1.role = None

    alert("You will now begin the simulation. \n\n"
          "Race 1 is a practice to familiarise you with the simulator. \n\n" 
          "Races 2-5 will show different race scenarios.\n\n"
          "Please complete all simulated races.", 
          title="Walkthrough")
    