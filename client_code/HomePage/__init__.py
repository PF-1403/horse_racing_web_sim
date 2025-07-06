from ._anvil_designer import HomePageTemplate
from anvil import *

class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.balance_bar_1.update_info(balance=200.0, race_number=3, total_races=7)

