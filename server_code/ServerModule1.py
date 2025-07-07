import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
from collections import defaultdict
import uuid
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
bet_log = {}

def find_favourite_id(competitors):
  if not competitors: 
    return None
    # Looks at the list of competitors and finds the horse which has the lowest odds in the list
  try: 
    return min(competitors, key=lambda x: float(x.get('initial_odds', 999)))['id']
  except (ValueError, TypeError):
    print("Warning: Could not determine favourite due to invalid odds format.")
    # Except looks like it just returns the first id in the list
    return competitors[0]['id'] if competitors else None

@anvil.server.callable
def get_race_spec(config_id="default"):
  competitors_set1 = [
    {"id": 1, "name": "Thunderstride", "color": "red", "initial_odds": 2.50},
    {"id": 2, "name": "Midnight Gambit", "color": "blue", "initial_odds": 3.50},
    {"id": 3, "name": "Blazing Comet", "color": "green", "initial_odds": 5.00},
    {"id": 4, "name": "Lucky Mirage", "color": "orange", "initial_odds": 7.50},
  ]
  competitors_set2 = [
    {"id": 1, "name": "Lightning Bolt", "color": "yellow", "initial_odds": 1.80},
    {"id": 2, "name": "Rolling Thunder", "color": "gray", "initial_odds": 4.00},
    {"id": 3, "name": "Dust Devil", "color": "brown", "initial_odds": 6.00},
    {"id": 4, "name": "Storm Chaser", "color": "blue", "initial_odds": 8.00},
  ]
  competitors_set3 = [
    {"id": 1, "name": "Fleet Flash", "color": "red", "initial_odds": 2.00},
    {"id": 2, "name": "Steady Strider", "color": "blue", "initial_odds": 3.20},
    {"id": 3, "name": "Dark Phantom", "color": "green", "initial_odds": 5.50},
    {"id": 4, "name": "Rapid Racer", "color": "orange", "initial_odds": 9.00},
  ]

  base_spec = {
    "track_length": 150,
    "in_play_window": 0.70
  }

  # Creates a copy here of the base spec for each race
  # base spec includes the basic track length and then and 'in play window'
  if config_id == "race1":
    spec = base_spec.copy()
    spec.update({
      "race_id": 1,
      "config_id": "race1",
      "race_type": "pre_win_predictable",
      "competitors": competitors_set1,
    })
    return spec

    # Includes extra call here to find the favourite of the competitor set being used
  elif config_id == "race2":
    spec = base_spec.copy()
    competitors = competitors_set2
    spec.update({
      "race_id": 2,
      "config_id": "race2",
      "race_type": "favourite_win_predictable",
      "competitors": competitors,
      "favourite_id": find_favourite_id(competitors)
    })
    return spec

  elif config_id == "race3":
    spec = base_spec.copy()
    spec.update({
      "race_id": "3",
      "config_id": "race3",
      "race_type": "pre_lead_then_lose",
      "competitors": competitors_set3,
    })
    return spec

  elif config_id == "race4":
    spec = base_spec.copy()
    spec.update({
      "race_id": "4",
      "config_id": "race4",
      "race_type": "pre_mid_lead_then_lose",
      "competitors": competitors_set1,
    })
    return spec
  elif config_id == "race5":
    spec = base_spec.copy()
    spec.update({
      "race_id": "5",
      "config_id": "race5",
      "race_type": "pre_late_surge_win_50",
      "competitors": competitors_set2,
    })
    return spec

  elif config_id == "race6":
    spec = base_spec.copy()
    spec.update({
      "race_id": "6",
      "config_id": "race6",
      "race_type": "pre_mid_surge_win_25",
      "competitors": competitors_set3,
    })
    return spec

  elif config_id == "race7":
    spec = base_spec.copy()
    spec.update({
      "race_id": "7",
      "config_id": "race7",
      "race_type": "pre_very_late_surge_win_75",
      "competitors": competitors_set1,
    })
    return spec

  else:
    print(f"Warning: Unknown config_id '{config_id}'. Using default random spec.")
    spec = base_spec.copy()
    spec.update({
      "race_id": 0,
      "config_id": "default",
      "race_type": "random",
      "competitors": competitors_set1,

    })
    return spec

@anvil.server.callable
def place_bet(competitor_id, stake, odds, balance):
  winnings = (stake * odds) - stake
  balance -= stake
  timestamp = datetime.utcnow().timestamp()

  log_entry = {
    "timestamp": timestamp,
    "comp_id": competitor_id,
    "stake": stake,
    "odds": odds,
    "potential_winnings": round(winnings, 2)
  }
  app_tables.bets.add_row(
    timestamp=timestamp,
    comp_id=competitor_id,
    stake=stake,
    odds=odds,
    potential_winnings=round(winnings, 2)
  )

  return balance, log_entry

@anvil.server.callable
def sum_logs():
  total_stakes = defaultdict(float)
  total_winnings = defaultdict(float)
  print("Getting logs from the data table...")
  
  for row in app_tables.bets.search():
    comp_id = str(row["comp_id"])
    stake = row["stake"]
    winnings = row["potential_winnings"]
    total_stakes[comp_id] += stake
    total_winnings[comp_id] += winnings

  return dict(total_stakes), dict(total_winnings)

@anvil.server.callable
def clear_bets_table():
  for row in app_tables.bets.search():
    row.delete()