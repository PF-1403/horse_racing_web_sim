from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Set each label from the corresponding item key
    self.label_id.text = str(self.item.get('id', ''))
    self.label_horse.text = self.item.get('horse_name', '')
    self.label_odds.text = self.item.get('odds', '')
    self.label_stake.text = f"£{self.item.get('stake', 0):.2f}"
    self.label_winnings.text = f"£{self.item.get('winnings', 0):.2f}"
