from ._anvil_designer import OddsTableTemplate
from anvil import *
import anvil.server

class OddsTable(OddsTableTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.]

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