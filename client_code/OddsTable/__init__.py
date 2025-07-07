from ._anvil_designer import OddsTableTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
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
        "winnings": 0.0
      }
      display_rows.append(row)
    self.repeating_panel_1.items = display_rows

  def populate_dynamic_odds(self, odds_dict):
    for row in self.repeating_panel_1.items:
      comp_id = row["id"]
      if comp_id in odds_dict:
        row["odds"] = odds_dict[comp_id]
    self.repeating_panel_1.items = self.repeating_panel_1.items

  def get_current_odds(self, comp_id):
    for row in self.repeating_panel_1.items:
      if row["id"] == comp_id:
        return row["odds"]
    Notification("Unable to select latest dynamic odds from table", style="warning").show()
    return

  def update_stakes(self, stakes, winnings):
    for id, amount in stakes.items():
      for row in self.repeating_panel_1.items:
        comp_id_row = row["id"]
        if comp_id_row == int(id):
          row["stake"] = amount
    
    for id, value in winnings.items():
      for row in self.repeating_panel_1.items:
        comp_id_row = row["id"]
        if comp_id_row == int(id):
          row["winnings"] = value
  
    self.repeating_panel_1.items = self.repeating_panel_1.items