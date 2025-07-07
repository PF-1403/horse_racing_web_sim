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

    # Make balance changes
    self.balance -= bet_amt
    self.update_balance_bar()
    Notification(f"Bet placed on horse {comp_id} for £{bet_amt:.2f}", style="success").show()