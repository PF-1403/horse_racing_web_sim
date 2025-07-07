from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import random

class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.balance_bar_1.update_info(balance=200.0, race_number=3, total_races=7)

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
    