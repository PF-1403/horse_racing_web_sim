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
    horse_images = {
      1: URLMedia('_/theme/blue_horse.png'),
      2: URLMedia('_/theme/green_horse.png'),
      3: URLMedia('_/theme/red_horse.png'),
      4: URLMedia('_/theme/yellow_horse.png')
    }
    
    display_rows = []
    for comp in competitors:
      row = {
        "id": comp["id"],
        "horse_image": horse_images[comp["id"]],
        "horse_name": comp["name"],
        "odds": comp["initial_odds"],
        "stake": 0.0,
        "winnings": 0.0
      }
      display_rows.append(row)
    self.repeating_panel_1.items = display_rows

  def populate_dynamic_odds(self, odds_dict):
    for row_comp in self.repeating_panel_1.get_components():
      comp_id = row_comp.item["id"]
      if comp_id in odds_dict:
        row_comp.item["odds"] = odds_dict[comp_id]
        row_comp.refresh_data_bindings()    

  def get_current_odds(self, comp_id):
    for row_comp in self.repeating_panel_1.get_components():
      if str(row_comp.item["id"]) == str(comp_id):
        odds = row_comp.item.get("odds")
        return odds
    Notification(f"Could not find odds for horse ID: {comp_id}", style="warning").show()
    return

  def update_stakes(self, stakes, winnings):
    for row_comp in self.repeating_panel_1.get_components():
      comp_id = row_comp.item["id"]
      if str(comp_id) in stakes:
        row_comp.item["stake"] = stakes[str(comp_id)]
      if str(comp_id) in winnings:
        row_comp.item["winnings"] = winnings[str(comp_id)]
      row_comp.refresh_data_bindings()
