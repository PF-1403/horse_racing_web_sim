from ._anvil_designer import RaceCanvasTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import random

class RaceCanvas(RaceCanvasTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.button_1.background = "#8adbdb"
    
    
    # Any code you write here will run before the form opens.
    self.horse_radius = 10
    self.horse_gap = 60
    self.num_horses = 4
    self.race_started = False

    # Initial horse positions
    self.horses = [{'x': 10, 'y': 50 + i * self.horse_gap} for i in range(self.num_horses)]

    # Set canvas size and force visual centering
    self.canvas_1.width = 800
    self.canvas_1.height = 300
    self.canvas_1.spacing_above = "none"
    self.canvas_1.spacing_below = "none"

  def form_show(self, **event_args):
  # Safe place to draw after layout is ready
    self.draw_canvas()

  def draw_canvas(self):
    canvas_width = self.canvas_1.get_width()
    canvas_height = self.canvas_1.get_height()

    if not canvas_width:
      return  # Wait until canvas is rendered

    # Clear canvas
    self.canvas_1.begin_path()
    self.canvas_1.fill_style = "white"
    self.canvas_1.fill_rect(0, 0, canvas_width, canvas_height)

    # Draw finish line
    self.finish_line = canvas_width - self.horse_radius - 10
    self.canvas_1.begin_path()
    self.canvas_1.stroke_style = "black"
    self.canvas_1.move_to(self.finish_line + 0.5, 0)
    self.canvas_1.line_to(self.finish_line + 0.5, canvas_height)
    self.canvas_1.stroke()

    # Draw horses
    for horse in self.horses:
      self.canvas_1.begin_path()
      self.canvas_1.fill_style = "blue"
      self.canvas_1.arc(horse['x'], horse['y'], self.horse_radius)
      self.canvas_1.fill()

  def button_1_click(self, **event_args):
    # Reset horse positions
    self.horses = [{'x': 10, 'y': 50 + i * self.horse_gap} for i in range(self.num_horses)]
    self.race_started = True
    self.timer_1.enabled = True
    self.draw_canvas()

  def timer_1_tick(self, **event_args):
    if not self.race_started:
      return

    race_ongoing = False
    for horse in self.horses:
      if horse['x'] < self.finish_line:
        horse['x'] = min(horse['x'] + random.randint(1, 5), self.finish_line)
      if horse['x'] < self.finish_line:
        race_ongoing = True

    self.draw_canvas()

    if not race_ongoing:
      self.timer_1.enabled = False
      self.race_started = False