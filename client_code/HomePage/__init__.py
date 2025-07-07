from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import random

class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.initialise_app()
    # Any code you write here will run before the form opens.
    self.place_bet_1.set_event_handler("x-place-bet", self.handle_place_bet)

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

  def calculate_dynamic_odds(self, competitors, positions):
    leader_position = max(positions.values())
    leader_progress = leader_position / self.finish_line
    odds = {}

    for comp in competitors:
      # Calculate relative positions
      current_position = positions.get(comp["id"], 0)
      progress = current_position / self.finish_line
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

    # TODO: Place bet here- call server function based upon odds
    # if static odds, place bet directly, if dynamic then do 'calculate_odds'
    if not self.race_active:
      # placeBet(comp_id, amt, static_odds)
      None
    else:
      #dynamic_odds = self.odds_table_1.get_current_odds(comp_id)
      # placeBet(comp_id, bet_amt, odds)
      None
    
    # Make balance changes
    self.balance -= bet_amt
    self.update_balance_bar()
    # TODO: update oddsTable
    #self.update_odds_table()
    Notification(f"Bet placed on horse {comp_id} for £{bet_amt:.2f}", style="success").show()