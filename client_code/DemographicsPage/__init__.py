from ._anvil_designer import DemographicsPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DemographicsPage(DemographicsPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.participant_id = anvil.server.call('get_or_make_id')
    # Any code you write here will run before the form opens.
    self.age_1.group_name = "age"
    self.age_2.group_name = "age"
    self.age_3.group_name = "age"
    self.age_4.group_name = "age"
    self.age_5.group_name = "age"
    self.age_6.group_name = "age"

    self.amt_1.group_name = "amount"
    self.amt_2.group_name = "amount"
    self.amt_3.group_name = "amount"
    self.amt_4.group_name = "amount"
    self.amt_5.group_name = "amount"

    self.exch_1.group_name = "exchange"
    self.exch_2.group_name = "exchange"
    self.exch_3.group_name = "exchange"

    self.odds_1.group_name = "odds"
    self.odds_2.group_name = "odds"
    self.odds_3.group_name = "odds"
    self.odds_4.group_name = "odds"
    self.odds_5.group_name = "odds"

    self.amt_1.group_name = "amount"
    self.amt_2.group_name = "amount"
    self.amt_3.group_name = "amount"
    self.amt_4.group_name = "amount"
    self.amt_5.group_name = "amount"

    self.gender_1.group_name = "gender"
    self.gender_2.group_name = "gender"
    self.gender_3.group_name = "gender"
    self.gender_4.group_name = "gender"

  def start_sim_click(self, **event_args):
    vals = self.get_all_values()
    for value in vals:
      if value is None:
        Notification("Please fill all form values!", style="danger").show()
        return

    with anvil.server.no_loading_indicator:
      anvil.server.call('store_demographics', vals, self.participant_id)
    open_form('HomePage')

  def get_all_values(self):
    gender = self.get_individual_values(self.gender_1, self.gender_2, self.gender_3, self.gender_4)
    age = self.get_individual_values(self.age_1, self.age_2, self.age_3, self.age_4, self.age_5, self.age_6)
    frequency = self.get_individual_values(self.freq_1, self.freq_2, self.freq_3, self.freq_4, self.freq_5)
    exchange = self.get_individual_values(self.exch_1, self.exch_2, self.exch_3)
    odds = self.get_individual_values(self.odds_1, self.odds_2, self.odds_3, self.odds_4, self.odds_5)
    amount = self.get_individual_values(self.amt_1, self.amt_2, self.amt_3, self.amt_4, self.amt_5)
    selected_vals = [gender, age, frequency, exchange, odds, amount]
    return selected_vals


  def get_individual_values(self, *radio_buttons):
    for button in radio_buttons:
      if button.selected:
        return button.value
    return None
