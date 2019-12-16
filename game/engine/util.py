# this module contains utility functions

import json

# checks if the mouse position is inside the sprite
def is_mouse_over(sprite, pos):
	if (sprite.x - sprite.width/2 <= pos[0] <= sprite.x + sprite.width/2) and \
		(sprite.y - sprite.height/2 <= pos[1] <= sprite.y + sprite.height/2):
		return True
	else:
		return False

# gets the rank of the Player's score based on the highscores
def get_rank(highscores, score):
	for i in range(len(highscores)):
		if score >= highscores[i]["score"]:
			return i
	return -1

# records the updated highscore data
def write_data(rank, score, name, file_path):
	new_data = read_file(file_path)
	new_data["highscores"].insert(rank, {"name": name.upper(), "score": score})
	new_data["highscores"] = new_data["highscores"][:-1]
	with open(file_path, "w") as score_data:
		json.dump(new_data, score_data, indent=4)

# reads a file
def read_file(file_path):
	with open(file_path, "r") as file:
		data = json.load(file)
	return data
		
# this ensures that the game window dimensions will always be 16:9 regardless of the device' screen resolution
def get_optimal_window_dimensions(device_width, device_height):
	width = device_width * 1600 // 1920
	height = device_height * 900 // 1080
	return width, height