import pyglet, random, math
from . import util, resources

# The Player is the player of the game, aka you, the user
class Player(object):
	def __init__(self, game_window):
		self.game_window = game_window

		self.lives = 5
		self.state = "dead" # the player state
		self.score = 0
		# container of the heart sprites
		self.heart_sprites = [Heart({"visible": False},
			x=i*self.game_window.width/12 + 30, y=0.125*self.game_window.height/8, 
			img=resources.heart, batch=self.game_window.gameplay_batch, 
			group=self.game_window.foreground_group)
			for i in range(self.lives)]

		# the name label on the main menu
		self.name_label = pyglet.text.Label(
			"ENTER NAME", font_name = 'Peace Sans', 
			x=2.75*self.game_window.width/12, y=4.5*self.game_window.height/8, 
			anchor_x="center", anchor_y="center",font_size=30, color=(255,255,255,255), 
			batch=self.game_window.menu_batch, group=self.game_window.text_group)

		# the input label of the gameplay
		self.input_label = pyglet.text.Label(
			"", font_name = 'Peace Sans', x=self.game_window.width/2, y=1.4*self.game_window.height/8, 
			anchor_x="center", anchor_y="center",font_size=35, color=(255,255,255,255), 
			batch=self.game_window.gameplay_batch, group=self.game_window.text_group)

		self.score_label_pos = [8*self.game_window.width/10, 0.375*self.game_window.height/7]
		# the player's score label
		self.score_label = pyglet.text.Label(
			"SCORE: {}".format(self.score), font_name = 'Peace Sans', 
			x=self.score_label_pos[0], y=self.score_label_pos[1], 
			anchor_x="center", anchor_y="center", font_size=30, color=(255,255,255,255), 
			batch=self.game_window.gameplay_batch, group=self.game_window.popup_text_group)

		# this allows the Player Object to have a KeyStateHandler
		self.key_handler = pyglet.window.key.KeyStateHandler()
		self.event_handlers = [self, self.key_handler]


	# the key state handler
	def on_key_press(self, symbol, modifiers):
		if self.state == "dead":
			if "ENTER NAME" in self.name_label.text:
				self.name_label.text = ""
			else:
				self.name_label.text = self.name_label.text[:-1]
			if symbol == pyglet.window.key.BACKSPACE:
				self.name_label.text = self.name_label.text[:-1]
			elif symbol == pyglet.window.key.RETURN and self.game_window.start_button.active:
				self.game_window.start_button.function()
			else:
				if chr(symbol).isalpha(): # should only register alpha characters
					self.name_label.text += chr(symbol).upper()
			self.name_label.text += "_" # this is the text cursor

		elif self.state == "alive" and self.lives > 0:
			self.input_label.text = self.input_label.text[:-1]
			if symbol == pyglet.window.key.BACKSPACE:
				self.input_label.text = self.input_label.text[:-1]
			elif symbol == pyglet.window.key.RETURN:
				for mga_words_obj in self.game_window.mga_words_objects:
					if self.input_label.text == mga_words_obj.label.text:
						resources.point_up_sfx.play()
						mga_words_obj.slide()
						if mga_words_obj.type == "masama":
							self.score += 3
						else:
							self.score += 1
				self.input_label.text = ""
					
			else:
				if chr(symbol).isalpha(): # should only register alpha characters
					self.input_label.text += chr(symbol)
			self.input_label.text += "_" # this is the text cursor

	# reset the player to its initial values
	def reset(self):
		self.lives = 5
		for heart in self.heart_sprites:
			heart.pop()
		self.score = 0
		self.name_label.text = "ENTER NAME"
		self.input_label.text = ""
		self.game_window.move_score_label(self.score_label, self.score_label_pos[0], self.score_label_pos[1])


# The heart sprites
class Heart(pyglet.sprite.Sprite):
	def __init__(self, attr, **kwargs):
		super().__init__(**kwargs)
		self.visible = attr["visible"]

	def pop(self):
		self.visible = False

	def reset(self):
		self.visible = True


# Mga Words are the words that need to be typed by the Player
# This class has two types: "di masama" (short words worth 1 point) and 
# "masama" (long words worth 3 points with side-to-side animation)
class MgaWords(pyglet.sprite.Sprite):
	def __init__(self, attr, **kwargs):
		super().__init__(**kwargs)
		self.window_width = attr["window_width"]
		self.window_height = attr["window_height"]
		self.mga_words = attr["mga_words"] # the list of words of a certain type ("di masama" and "masama")
		random.shuffle(self.mga_words)
		self.initial_pos = [self.x , self.y]
		self.animation_counter = 0 # the counter used in the side-to-side animation
		self.count = 0 # counts the number of words of its type that appeared
		self.type = attr["type"]
		self.xy_velocity = attr["xy_velocity"]
		self.initial_xy_velocity = self.xy_velocity[:]
		self.image.anchor_x = self.width / 2
		self.image.anchor_y = self.height / 2
		self.color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

		if self.type == "masama":
			self.scale_x = attr["window_scale_x"] * 1.75
		else:
			self.scale_x = attr["window_scale_x"]

		self.scale_y = attr["window_scale_y"]
		self.label = pyglet.text.Label(self.mga_words[self.count], font_name = 'Peace Sans', 
			x=self.x, y=self.y, anchor_x="center", anchor_y="center",font_size=attr["font_size"], 
			color=(255,255,255,255), batch=self.batch, group=attr["text_group"])


	def update(self, dt):
		self.y += self.xy_velocity[1] * dt
		self.x += self.xy_velocity[0] * dt
		
		if self.type == "masama" and self.xy_velocity[0] == 0:
			self.animate(dt) # the side-to-side animation
		
		self.label.x = int(self.x)
		self.label.y = int(self.y)
		
		if self.is_outside_screen():
			self.pop()

		# increase speed every three words
		if self.count % 3 == 0 and self.count != 0:
			if self.type == "di_masama":
				self.xy_velocity[1] -= 20 * dt
			else:
				self.xy_velocity[1] -= 10 * dt

	# the slide animation that occurs when the Player entered the correct word
	def slide(self):
		if self.type == "di_masama":
			self.xy_velocity[0] = -5000
		else:
			self.xy_velocity[0] = 5000


	# checks if the object is already outside the screen after doing the slide() animation
	def is_outside_screen(self):
		if self.x + self.width < 0 or self.x - self.width > self.window_width:
			return True
		return False


	# this is the side-to-side animation of the Masasamang Mga Words
	# based on the sine function where the "angle" is the animation_counter
	def animate(self, dt):
		amplitude = 100
		self.x = self.initial_pos[0] + (math.sin(self.animation_counter) * amplitude)
		self.animation_counter += 1.75 * math.pi * dt

	# resets the object to its initial values once the game is over
	def reset(self):
		self.count = 0
		random.shuffle(self.mga_words)
		self.x = self.initial_pos[0]
		self.y = self.initial_pos[1]


	# pops the object back to the top when either the player entered the correct word or 
	# when the object has reached the bottom of the screen
	def pop(self):
		self.animation_counter = 0
		self.xy_velocity[0] = 0
		self.color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
		self.x = self.initial_pos[0]
		self.y = self.initial_pos[1]
		self.label.y = int(self.y)
		self.count += 1
		self.label.text = self.mga_words[self.count % len(self.mga_words)]
