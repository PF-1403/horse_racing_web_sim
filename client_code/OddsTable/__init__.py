from ._anvil_designer import OddsTableTemplate
from anvil import *
import anvil.server

class OddsTable(OddsTableTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.]
    # self.repeating_panel_1.items = [
    #   {
    #     "id": 1,
    #     "horse_name": "Lightning",
    #     "odds": "4/1",
    #     "stake": 10,
    #     "potential_winnings": 40
    #   },
    #   {
    #     "id": 2,
    #     "horse_name": "Thunder",
    #     "odds": "5/2",
    #     "stake": 15,
    #     "potential_winnings": 52.5
    #   }
    # ]
  def populate_static_odds(self, competitors):
    display_rows = []
    for comp in competitors:
      row = {
        "id": comp["id"],
        "horse_name": comp["name"],
        "odds": comp["initial_odds"],
        "stake": 0.0,
        "potential_winnings": 0.0
      }
      display_rows.append(row)
    self.repeating_panel_1.items = display_rows