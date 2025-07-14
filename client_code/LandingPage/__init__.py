from ._anvil_designer import LandingPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import uuid

class LandingPage(LandingPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.participant_id = anvil.server.call('get_or_make_id')

  def start_button_click(self, **event_args):
    open_form('HomePage')
