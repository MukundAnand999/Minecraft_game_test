from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image
import numpy as np
import random

app = Ursina()

selected_block = "grass"

player = FirstPersonController(
  mouse_sensitivity=Vec2(100, 100),
  position=(0, 5, 0)
)

block_textures = {
  "grass": load_texture("assets/textures/groundEarth.png"),
  "dirt": load_texture("assets/textures/groundMud.png"),
  "stone": load_texture("assets/textures/wallStone.png"),
  "bedrock": load_texture("assets/textures/stone07.png")
}

class Block(Entity):
  def __init__(self, position, block_type):
    super().__init__(
      position=position,
      model="assets/models/block_model",
      scale=1,
      origin_y=-0.5,
      texture=block_textures.get(block_type),
      collider="box"
    )
    self.block_type = block_type

mini_block = Entity(
  parent=camera,
  model="assets/models/block_model",
  texture=block_textures.get(selected_block),
  scale=0.2,
  position=(0.35, -0.25, 0.5),
  rotation=(-15, -30, -5)
)

# Load the heightmap image
heightmap = Image.open("map.png").convert("L")
heightmap_data = np.array(heightmap)

min_height = -5
scale_factor = 7.5

# Generate the terrain using the heightmap
world_range = heightmap_data.shape[0]
for x in range(world_range):
  for z in range(world_range):
    height = heightmap_data[x, z] / 255 * scale_factor
    height = int(height)
    for y in range(height, min_height - 1, -1):
      if y == min_height:
        block = Block((x, y + min_height, z), "bedrock")
      elif y == height:
        block = Block((x, y + min_height, z), "grass")
      elif height - y > 2:
        block = Block((x, y + min_height, z), "stone")
      else:
        block = Block((x, y + min_height, z), "dirt")

def input(key):
  global selected_block
  if key == 'left mouse down':
    hit_info = raycast(camera.world_position, camera.forward, distance=10)
    if hit_info.hit:
      block = Block(hit_info.entity.position + hit_info.normal, selected_block)
  if key == 'right mouse down' and mouse.hovered_entity:
    if not mouse.hovered_entity.block_type == "bedrock":
      destroy(mouse.hovered_entity)
  if key == '1':
    selected_block = "grass"
  if key == '2':
    selected_block = "dirt"
  if key == '3':
    selected_block = "stone"

def update():
  mini_block.texture = block_textures.get(selected_block)

app.run()
