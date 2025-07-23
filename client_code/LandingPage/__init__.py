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
    self.label_2.align = "center"
    self.label_2.text = ("My name is Peter Fox, and I am an MSc Data Science student at the "
                        "University of Bristol.\n" 
                        "I am currently preparing my final thesis, which aims to improve upon Prof. Dave Cliff's work to \n"
                        "develop a simulated in-play horse betting exchange, and my particular focus is on human betting behaviours.\n\n"
                        "This simulation hopes to aggregate your anonymised simulation responses to create 'agents' to be used in the \n"
                        "exchange to bet in human-like ways and improve the overall integrity of the project.\n\n"
                        "The simulation comprises of a short survey, followed by 5 mock horse races which you place bets on\n"
                        "before and during the races.\n"
                        "Results for both the survey and simulation do not store any identifying information, and your resonses will\n"
                        "be aggregated across all respondents.\n\n"
                        "The simulation falls under the University of Bristol Ethics Application 15208.\n\n"
                        "Please press the 'Begin Experiment' button below to continue."
                        )
  def start_button_click(self, **event_args):
    open_form('DemographicsPage')
