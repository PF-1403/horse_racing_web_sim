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

    if 'participant_id' not in anvil.users.SessionStorage:
      new_id = str(uuid.uuid4())
      anvil.users.SessionStorage["participant_id"] = new_id
      anvil.server.call('store_participant_id',new_id)

  def start_button_click(self, **event_args):
    open_form('HomePage')
