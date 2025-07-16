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
    

    # Set canvas size and force visual centering
    self.canvas_1.width = 800
    self.canvas_1.height = 320
    self.canvas_1.spacing_above = "none"
    self.canvas_1.spacing_below = "none"
  
    self.horse_radius = 16
    self.num_horses = 4


    self.add_number = 24
    self.lane_size = 80
    # Initial horse positions
    self.horses = [{'id': i + 1,'x': 16, 'y': self.horse_radius + self.add_number + (i * self.lane_size)} for i in range(self.num_horses)]

    # Set up horse images
    self.horse_images = [
      URLMedia('_/theme/blue_horse.png'),
      URLMedia('_/theme/green_horse.png'),
      URLMedia('_/theme/red_horse.png'),
      URLMedia('_/theme/yellow_horse.png')
    ]

  def form_show(self, **event_args):
    # Safe place to draw after layout is ready
    self.draw_canvas(self.horses)

  def draw_canvas(self, horse_loc):
    canvas_width = self.canvas_1.get_width()
    canvas_height = self.canvas_1.get_height()

    if not canvas_width:
      return  # Wait until canvas is rendered

    # Clear canvas
    self.canvas_1.fill_style = "white"
    self.canvas_1.fill_rect(0, 0, canvas_width, canvas_height)

    # Draw finish line
    self.finish_line = canvas_width - self.horse_radius - 10
    self.canvas_1.begin_path()
    self.canvas_1.stroke_style = "black"
    self.canvas_1.move_to(self.finish_line + 0.5, 0)
    self.canvas_1.line_to(self.finish_line + 0.5, canvas_height)
    self.canvas_1.stroke()

    # Draw start line
    self.start_line = 2 * self.horse_radius
    self.canvas_1.begin_path()
    self.canvas_1.stroke_style = "black"
    self.canvas_1.move_to(self.start_line + 0.5, 0)
    self.canvas_1.line_to(self.start_line + 0.5, canvas_height)
    self.canvas_1.stroke()

    # Draw bets line
    html_canvas = anvil.js.get_dom_node(self.canvas_1)
    context = html_canvas.getContext('2d')
    context.setLineDash([5, 15])
    self.start_line = 0.8 * self.finish_line
    self.canvas_1.begin_path()
    self.canvas_1.stroke_style = "black"
    self.canvas_1.move_to(self.start_line + 0.5, 0)
    self.canvas_1.line_to(self.start_line + 0.5, canvas_height)
    self.canvas_1.stroke()
    context.setLineDash([])

    # Draw lanes
    lanes = [80, 160, 240]
    for lane in lanes:
      self.canvas_1.begin_path()
      self.canvas_1.stroke_style = "black"
      self.canvas_1.move_to(0, lane + 0.5)
      self.canvas_1.line_to(canvas_width, lane + 0.5)
      self.canvas_1.stroke()      
    
    # Draw horses
    for horse in horse_loc:
      index = self.horses.index(horse)
      img_url = self.horse_images[index]

      self.canvas_1.draw_image(img_url,
                              horse['x'] - self.horse_radius,
                              horse['y'] - self.horse_radius,
                              self.horse_radius * 2,
                              self.horse_radius * 2)

  def button_1_click(self, **event_args):
    # Disable button and raise event to start the race
    self.button_1.enabled = False
    self.raise_event("x-start-race", horses=self.horses, finish_line=self.finish_line)

  def reset_button(self):
    self.button_1.enabled = True

  def reset_canvas(self):
    self.horses = [{'id': i + 1,'x': 16, 'y': self.horse_radius + self.add_number + (i * self.lane_size)} for i in range(self.num_horses)]
    self.draw_canvas(self.horses)