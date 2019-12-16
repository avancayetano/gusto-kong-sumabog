
# Gusto Kong Sumabog

# font used: "Peace Sans" by Jovanny Lemonad, licensed under the SIL Open Font License
# pyglet learning resource: https://pyglet.readthedocs.io/en/stable/ by Alex Holkner

# Artworks derived from (screenshot):
# [ Pinoy Big Brother]. (2018, October 27). PBB balikbahay: Boys vs. girls food war. Retrieved from https://www.youtube.com/watch?v=8ylELL7r7UE
# Audio (game_over_music.wav) derived from: 
# [ Pinoy Big Brother]. (2018, October 27). PBB balikbahay: Boys vs. girls food war. Retrieved from https://www.youtube.com/watch?v=8ylELL7r7UE



import pyglet
from engine import game_objects, window_objects, resources, util

class GameWindow(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		pyglet.clock.schedule_interval(self.update, 1/60)
		# the scaling below is necessary so that the window ratio will always be 16:9 in any screen resolution
		self.window_scale_x = self.width / 1600
		self.window_scale_y = self.height / 900

		self.gameplay_batch = pyglet.graphics.Batch()
		self.menu_batch = pyglet.graphics.Batch()

		# layers
		self.background_group = pyglet.graphics.OrderedGroup(0)
		self.foreground_group = pyglet.graphics.OrderedGroup(1)
		self.text_group = pyglet.graphics.OrderedGroup(2)

		# layers for popup windows (such as the help window)
		self.popup_group = pyglet.graphics.OrderedGroup(3)
		self.popup_button_group = pyglet.graphics.OrderedGroup(4)
		self.popup_text_group = pyglet.graphics.OrderedGroup(5)

		# the music player
		self.music_player = pyglet.media.Player()
		self.music_player.loop = True
		self.music_player.queue(resources.main_menu_music)
		self.music_player.queue(resources.gameplay_music)
		self.music_player.queue(resources.game_over_music)
		self.music_player.play()

		# the background image for the menu screen
		self.menu_screen = window_objects.WindowObject(
			{"target_pos": [self.width/2, self.height/2], "animation_speed": 5000, "animation": "slide",
			"window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y, "do_animation": True}, 
			img=resources.menu_screen, x=-self.width/2, y=self.height/2, 
			batch=self.menu_batch, group=self.background_group)

		# the background img for the gameplay screen
		self.gameplay_screen = window_objects.WindowObject(
			{"target_pos":[self.width/2, self.height/2], "animation_speed": 5000, "animation": "slide",
			"window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y, "do_animation": True}, 
			img=resources.gameplay_screen, x=-self.width/2, y=self.height/2, 
			batch=self.gameplay_batch, group=self.background_group)

		self.help_window = window_objects.WindowObject(
			{"target_pos": [self.width/2, self.height/2], "animation_speed": 5000, "animation": "slide",
			"window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y, "do_animation": False,
			"exit_pos": [self.width/2, 2*self.height]},
			img=resources.help_window, x=self.width/2, y=-self.height,
			batch=self.menu_batch, group=self.popup_group)

		# the explosion sprite
		self.explosion = window_objects.WindowObject(
			{"target_pos": [self.width/2, self.height/2], "animation_speed": 7, "animation": "explode",
			"window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y, "do_animation": False},
			img=resources.explosion, x=self.width/2, y=self.height/2,
			batch=self.gameplay_batch, group=self.popup_group)

		# the next five objects are the buttons
		self.start_button = window_objects.Button(
			{"target_pos": [2.75*self.width/12, 3.5*self.height/8], "animation_speed": 2000, "animation": "slide", "function": self.start,
			"window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y,
			"text": "START", "text_group": self.text_group, "font_size": 30*self.window_scale_x, "do_animation": True, "color": (196, 69, 105)},
			img=resources.button_container,x=-500, y=3.5*self.height/8,
			batch=self.menu_batch, group=self.foreground_group)

		self.help_button = window_objects.Button(
			{"target_pos": [2.75*self.width/12, 2.5*self.height/8], "animation_speed": 2000, "animation": "slide", "function": self.help,
			"text": "HELP", "window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y,
			"text_group": self.text_group, "font_size": 30*self.window_scale_x, "do_animation": True, "color": (207, 106, 135)},
			img=resources.button_container, x=-1000, y=2.5*self.height/8,
			batch=self.menu_batch, group=self.foreground_group)

		self.quit_button = window_objects.Button(
			{"target_pos": [2.75*self.width/12, 1.5*self.height/8], "animation_speed": 2000, "animation": "slide", "function": self.quit,
			"text": "QUIT", "window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y,
			"text_group": self.text_group, "font_size": 30*self.window_scale_x, "do_animation": True, "color": (230, 103, 103)},
			img=resources.button_container, x=-1500, y=2*self.height/8,
			batch=self.menu_batch, group=self.foreground_group)

		self.back_button = window_objects.Button(
			{"target_pos": [self.width/2, self.height/8], "animation_speed": 5000, "animation": "slide", "function": self.back,
			"text": "BACK", "window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y,
			"text_group": self.popup_text_group, "font_size": 30*self.window_scale_x, "do_animation": False, "color": (255, 255, 255), 
			"exit_pos": [self.width/2, self.height + 200], "font_color": (225, 82, 95, 255)},
			img=resources.button_container, x=self.width/2, y=-self.height,
			batch=self.menu_batch, group=self.popup_button_group)

		self.retry_button = window_objects.Button(
			{"target_pos": [self.width/2, 2*self.height/8], "animation_speed": 3000, "animation": "slide", "function": self.retry,
			"text": "RETRY", "window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y,
			"text_group": self.popup_text_group, "font_size": 30*self.window_scale_x, "do_animation": False, "color": (179, 57, 57)},
			img=resources.button_container, x=-500, y=2*self.height/8,
			batch=self.gameplay_batch, group=self.popup_button_group)

		# container for the window_objects (buttons and images)
		# the keys "dead" and "alive" refer to the player state, whether the player is currently playing (alive) or not (dead)
		self.window_objects = {
			"dead": [self.menu_screen, self.start_button, self.help_button, self.quit_button, self.back_button, self.help_window],
			"alive": [self.gameplay_screen, self.explosion, self.retry_button],
		}

		self.buttons = [self.start_button, self.help_button, self.retry_button, self.quit_button, self.back_button]
		
		mga_words_data = util.read_file("resources/data/mga_words.json")

		self.mga_words_objects = [
			game_objects.MgaWords({"window_width": self.width, "window_height": self.height, 
				"mga_words": mga_words_data["di_masama"], "text_group": self.text_group, "type": "di_masama", "xy_velocity": [0, -100], 
				"window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y, "font_size": 30*self.window_scale_x}, 
				img=resources.button_container, x=3*self.width/12,y=self.height+100, 
				batch=self.gameplay_batch, group=self.foreground_group),
			game_objects.MgaWords({"window_width": self.width, "window_height": self.height, 
				"mga_words": mga_words_data["masama"], "text_group": self.text_group,"type": "masama", "xy_velocity": [0, -50], 
				"window_scale_x": self.window_scale_x, "window_scale_y": self.window_scale_y, "font_size": 30*self.window_scale_x},
				img=resources.button_container, x=9*self.width/12, y=self.height+100, 
				batch=self.gameplay_batch, group=self.foreground_group)
		]

		# the player of the game
		self.player = game_objects.Player(self)

		# adds the event handler of the Player (on_key_press) on the window event handlers
		for handler in self.player.event_handlers:
			self.push_handlers(handler)

		self.highscores_data = util.read_file("resources/data/highscores.json")["highscores"]

		self.score_labels = []
		self.update_score_labels(self.highscores_data)

		self.freezed = False # the gameplay will freeze once the game is over (when player.lives == 0)


	# the main game loop, controls the state of the game
	# updates the game objects and the window objects based on the player state (dead or alive)
	def update(self, dt):
		if self.player.state == "alive":
			for mga_words_obj in self.mga_words_objects:
				mga_words_obj.update(dt)
				if mga_words_obj.y + mga_words_obj.height < 0:
					mga_words_obj.pop()
					if self.player.lives > 0:
						resources.point_deduction_sfx.play()
						self.player.lives -= 1
						self.player.heart_sprites[self.player.lives].pop()
			
			# freezes the game when the game is over (player.lives == 0)
			if self.player.lives == 0 and not self.freezed:
				self.play_next_music(resources.gameplay_music, 0.5)
				self.freeze()
				self.explosion.do_animation = True
				self.retry_button.do_animation = True
				self.move_score_label(self.player.score_label, self.width / 2, self.height / 2.3) # move to the center
			self.player.score_label.text = "SCORE: {}".format(self.player.score)

		for obj in self.window_objects[self.player.state]:
			obj.animate(dt)


	# freezes any game movement once the game is over
	def freeze(self):
		self.gameplay_screen.color = (120, 120, 120)
		for mga_words_obj in self.mga_words_objects:
			mga_words_obj.count = 0
			mga_words_obj.pop()
			mga_words_obj.xy_velocity[1] = 0
		self.freezed = True


	# unfreezes the game
	def unfreeze(self):
		self.gameplay_screen.color = (255, 255, 255)
		for mga_words_obj in self.mga_words_objects:
			mga_words_obj.xy_velocity = mga_words_obj.initial_xy_velocity[:]
		self.freezed = False


	def play_next_music(self, current_music, volume):
		self.music_player.next_source()
		self.music_player.play()
		self.music_player.volume = volume
		self.music_player.queue(current_music)


	def move_score_label(self, score_label, x, y):
		score_label.x = x
		score_label.y = y

	# update the highscore labels or create them if they don't exist yet
	def update_score_labels(self, data):
		if len(self.score_labels) == 0:
			for idx, name_score in enumerate(data):
				score_label = pyglet.text.Label("{}: {} - {}".format(idx + 1, name_score["name"], name_score["score"]), 
					x=(window_width//3)*idx + window_width//6, y=40, anchor_x="center", anchor_y="center", font_name = 'Peace Sans',
					font_size=30, color=(255,255,255,255), batch=self.menu_batch, group=self.text_group)
				self.score_labels.append(score_label)
		else:
			for idx, name_score in enumerate(data):
				self.score_labels[idx].text = "{}: {} - {}".format(idx + 1, name_score["name"], name_score["score"])


	def toggle_buttons(self, buttons):
		for button in buttons:
			button.active = not button.active

	# below are the 5 button functions of the 5 buttons
	# start the game if the name is valid. this changes the player state to "alive"
	def start(self):
		if not("ENTER NAME" in self.player.name_label.text) and self.player.name_label.text != "":
			self.play_next_music(resources.main_menu_music, 0.2)
			self.player.state = "alive"
			for heart in self.player.heart_sprites:
				heart.reset()
			for obj in self.window_objects[self.player.state]:
				obj.reset()
			self.unfreeze()

		else:
			self.player.name_label.text = "*ENTER NAME!*"
	
	# return to the main menu. changes the player state to "dead"
	def retry(self):
		self.play_next_music(resources.game_over_music, 1)
		self.player.state = "dead"
		rank = util.get_rank(self.highscores_data, self.player.score)
		if rank >= 0:
			util.write_data(rank, self.player.score, self.player.name_label.text[:-1], "resources/data/highscores.json")
			self.highscores_data = util.read_file("resources/data/highscores.json")["highscores"]
			self.update_score_labels(self.highscores_data)
		self.player.reset()

		self.explosion.do_animation = False
		self.retry_button.do_animation = False

		for obj in self.window_objects[self.player.state]:
			obj.reset()
		for mga_words_obj in self.mga_words_objects:
			mga_words_obj.reset()

	# toggle the help window
	def help(self):
		self.toggle_buttons(self.buttons[:-1])
		self.back_button.reset()
		self.help_window.reset()
		self.back_button.do_animation = True
		self.help_window.do_animation = True
		self.menu_screen.color = (120, 120, 120)

	# close the help window
	def back(self):
		self.toggle_buttons(self.buttons[:-1])
		self.help_window.on_display = False
		self.back_button.do_animation = True
		self.help_window.do_animation = True
		self.menu_screen.color = (255, 255, 255)

	# close the game
	def quit(self):
		pyglet.app.exit()


	def on_draw(self):
		self.clear()
		if self.player.state == "dead":
			self.menu_batch.draw()
		else:
			self.gameplay_batch.draw()

	# mouse press handler
	def on_mouse_press(self, x, y, button, modifiers):
		for button in self.buttons:
			if util.is_mouse_over(button, (x, y)) and button.active:
				button.function() # call the button's function


	# mouse motion handler
	def on_mouse_motion(self, x, y, dx, dy):
		self.set_mouse_cursor(cursor=None)
		for button in self.buttons:
			if util.is_mouse_over(button, (x, y)) and button.active:
				self.set_mouse_cursor(cursor=self.get_system_mouse_cursor(self.CURSOR_HAND))
				button.focus() # enlarges the button
			else:
				button.defocus()


if __name__ == "__main__":
	screen = pyglet.canvas.get_display().get_default_screen() # gets the screen resolution
	window_width, window_height = util.get_optimal_window_dimensions(screen.width, screen.height)
	window = GameWindow(window_width, window_height, "Gusto Kong Sumabog", resizable=False)
	pyglet.app.run()