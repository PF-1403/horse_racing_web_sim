from ._anvil_designer import PlaceBetTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class PlaceBet(PlaceBetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def competitor_text_pressed_enter(self, **event_args):
    self.bet_button_click()

  def bet_text_pressed_enter(self, **event_args):
    self.bet_button_click()

  def bet_button_click(self, **event_args):
    # Validate that the competitor ID is an int and populated
    comp_id = self.competitor_text.text
    bet_amt = self.bet_text.text

    if not comp_id and bet_amt:
      Notification("Please enter a value for all fields.", style="warning").show()
      return

    try:
      comp_id = int(comp_id)
      bet_amt = float(bet_amt)
    except ValueError:
      Notification("Please enter valid numerical values.", style="warning").show()
      return

    if bet_amt < 0:
      Notification("Please enter a positive bet amount.", style="warning").show()
      return

    self.raise_event("x-place-bet", comp_id=comp_id, bet_amt=round(bet_amt,2)) 
    self.clear_vals()

  def clear_vals(self):
    self.competitor_text.text = ""
    self.bet_text.text = ""
    