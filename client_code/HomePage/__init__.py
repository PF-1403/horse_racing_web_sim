from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random

class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.initialise_app()
    self.race_started = False
    # Any code you write here will run before the form opens.
    self.place_bet_1.set_event_handler("x-place-bet", self.handle_place_bet)
    self.race_canvas_1.set_event_handler("x-start-race", self.start_race)

  def initialise_app(self):
    self.balance = 1000.0
    self.race_index = 0
    self.finish_line = 100
    self.race_active = False
    self.race_ids = ["race1", "race2", "race3", "race4", "race5", "race6", "race7"]
    random.shuffle(self.race_ids)
    self.bets = []
    print("Initialisation of app is complete!")

    self.load_next_race()

  def load_next_race(self):
    anvil.server.call('clear_bets_table')
    race_id = self.race_ids[self.race_index]
    self.race_spec = anvil.server.call('get_race_spec',race_id)
    print(f'Race Loaded! \nRace number {self.race_index+1}/{len(self.race_ids)}')
    print(f'Race spec: {self.race_spec["config_id"]}')

    #TODO: Create this race_spec function
    #self.race_canvas_1.load_race_spec(self.race_spec)
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

    if not self.race_active:
      static_odds = next((c["initial_odds"] for c in self.race_spec["competitors"] if c["id"] == comp_id), None)
      self.balance, bet_log = anvil.server.call('place_bet', comp_id, bet_amt, static_odds, self.balance)
      Notification(f"Bet placed on horse {comp_id} for £{bet_amt:.2f} at odds of {static_odds:.2f}", style="success").show()
      print("Successfully placed static bet")
    else:
      dynamic_odds = self.odds_table_1.get_current_odds(comp_id)
      self.balance, bet_log = anvil.server.call('place_bet', comp_id, bet_amt, dynamic_odds, self.balance)
      Notification(f"Bet placed on horse {comp_id} for £{bet_amt:.2f} at odds of {dynamic_odds:.2f}", style="success").show()
      print("Successfully placed dynamic bet")

    self.update_stakes()
    self.update_balance_bar()

  def start_race(self, **event_args):
    # Establish initial horse location, show race started
    self.horse_location = event_args['horses']
    self.finish_line = event_args['finish_line']
    self.race_started = True 
    self.race_timer.enabled = True
    
  def race_timer_tick(self, **event_args):
    if not self.race_started:
      return

    race_won = False
    race_ongoing = False
    for horse in self.horse_location:
      if horse['x'] < self.finish_line:
        horse['x'] = min(horse['x'] + random.randint(1, 5), self.finish_line)
        race_ongoing = True
      elif horse['x'] == self.finish_line and not race_won:
        race_winner = horse['id']
        race_won = True
    self.race_canvas_1.draw_canvas(self.horse_location)
    
    ## Now populate dynamic odds here ##
    self.calculate_dynamic_odds(self.race_spec['competitors'], self.horse_location)

    if not race_ongoing:
      self.race_timer.enabled = False
      self.race_started = False
      self.race_complete(race_winner)

  def calc_and_disp_results(self, race_winner):
    pass

  def log_results(self):
    pass

  def race_complete(self, race_winner):
    self.calc_and_disp_results(race_winner)
    self.log_results()
  
    # Add 1 to race index and decide on logic
    self.race_index += 1
    if self.race_index > len(self.race_ids):
      # Notification
      # move to final form
      pass
    else:
      self.load_next_race()