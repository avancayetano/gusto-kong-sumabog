import pyglet
from . import util, resources

# WindowObjects are the interface' objects, which are objects that are not part of the gameplay.
# This include the buttons and background images
class WindowObject(pyglet.sprite.Sprite):
	def __init__(self, attr, **kwargs):
		super().__init__(**kwargs)

		self.image.anchor_x = self.width / 2
		self.image.anchor_y = self.height / 2

		self.animation = attr["animation"]
		self.do_animation = attr["do_animation"]
		self.do_animation_buffer = self.do_animation # a buffer variable, used to reset the do_animation variable to its initial value
		self.animation_speed = attr["animation_speed"]
		
		if self.animation == "explode":
			self.initial_scale = [0, 0]
			self.target_scale = [attr["window_scale_x"], attr["window_scale_y"]]

		elif self.animation == "slide":
			self.target_pos = attr["target_pos"]
			self.target_pos_buffer = self.target_pos[:] # a buffer variable, used to reset the target_pos variable to its initial value
			self.initial_scale = [attr["window_scale_x"], attr["window_scale_y"]]
			self.initial_pos = [self.x, self.y]
			self.exit_pos = attr.get("exit_pos", self.target_pos)

		self.scale_x = self.initial_scale[0]
		self.scale_y = self.initial_scale[1]


	# animate the object depending on its of type of animation
	def animate(self, dt):
		if self.do_animation:
			if self.animation == "slide":
				self.slide(dt)
			elif self.animation == "explode":
				self.explode(dt)


	# the slide animation
	def slide(self, dt):
		if self.x < self.target_pos[0]:
			self.x += int(self.animation_speed * dt)
		if self.y < self.target_pos[1]:
			self.y += int(self.animation_speed * dt)
		if self.x > self.target_pos[0]:
			self.x = self.target_pos[0]
		if self.y > self.target_pos[1]:
			self.y = self.target_pos[1]

		# when the object reached its target position, the animation will stop, hence do_animation = False
		if self.x == self.target_pos[0] and self.y == self.target_pos[1]:
			self.on_display = True
			self.target_pos = self.exit_pos
			self.do_animation = False

		if isinstance(self, Button):
			self.label.x = self.x
			self.label.y = self.y


	# the explode animation
	def explode(self, dt):
		if self.scale_x < self.target_scale[0]:
			self.scale_x += self.animation_speed * dt
		if self.scale_y < self.target_scale[1]:
			self.scale_y += self.animation_speed * dt
		if self.scale_x > self.target_scale[0]:
			self.scale_x = self.target_scale[0]
		if self.scale_y > self.target_scale[1]:
			self.scale_y = self.target_scale[1]

		# when the object reached its target scale, the animation will stop, hence do_animation = False
		if self.scale_x == self.target_scale[0] and self.scale_y == self.target_scale[1]:
			self.on_display = True
			self.do_animation = False


	# resets the object to its initial values
	def reset(self):
		if self.animation == "slide":
			self.target_pos = self.target_pos_buffer[:]
			
			self.x = self.initial_pos[0]
			self.y = self.initial_pos[1]
			if isinstance(self, Button):
				self.label.x = self.x
				self.label.y = self.y
		elif self.animation == "explode":
			self.scale_x = self.initial_scale[0]
			self.scale_y = self.initial_scale[1]

		self.do_animation = self.do_animation_buffer


# A WindowObject that is interactive (clickable)
class Button(WindowObject):
	def __init__(self, attr, **kwargs):
		super().__init__(attr, **kwargs)
		self.function = attr["function"] # the function of the button that will be executed when clicked
		self.active = True
		self.color = attr["color"]
		self.font_color = attr.get("font_color", (255,255,255,255))
		self.label = pyglet.text.Label(attr["text"], font_name = 'Peace Sans', x=self.x, y=self.y, anchor_x="center", anchor_y="center",
			font_size=attr["font_size"], color=self.font_color, batch=self.batch, group=attr["text_group"])

	# enlarges the button
	def focus(self):
		if self.scale == 1:
			self.scale = self.scale * 1.5
			self.label.font_size = self.label.font_size * 1.5

	# returns the button to its original size
	def defocus(self):
		if self.scale != 1:
			self.scale = self.scale / 1.5
			self.label.font_size = self.label.font_size / 1.5
