from ._anvil_designer import BalanceBarTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

class BalanceBar(BalanceBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def update_info(self, balance, race_number, total_races):
    self.lbl_balance.text = f"Balance (£): {balance:.2f}"
    self.lbl_races.text = f"Race Number: {race_number}/{total_races}"