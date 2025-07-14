from ._anvil_designer import EndFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EndForm(EndFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.participant_id = anvil.server.call('get_or_make_id')
    # Any code you write here will run before the form opens.
