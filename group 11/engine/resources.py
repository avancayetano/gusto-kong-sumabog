import pyglet

pyglet.resource.path = ["resources/visuals"]
pyglet.resource.reindex()

menu_screen = pyglet.resource.image("new_menu_screen.png")
gameplay_screen = pyglet.resource.image("gameplay_screen.png")
button_container = pyglet.resource.image("container.png")
heart = pyglet.resource.image("heart.png")
explosion = pyglet.resource.image("game_over.png")
help_window = pyglet.resource.image("help_window.png")

gameplay_music = pyglet.media.load("resources/audio/gameplay_music.wav", streaming=False)
main_menu_music = pyglet.media.load("resources/audio/menu_music.wav", streaming=False)
game_over_music = pyglet.media.load("resources/audio/game_over_music.wav", streaming=False)

point_deduction_sfx = pyglet.media.load("resources/audio/point_deduction_sfx.wav", streaming=False)
point_up_sfx = pyglet.media.load("resources/audio/point_up_sfx.wav", streaming=False)

pyglet.font.add_directory('resources/visuals')
peace_sans_font = pyglet.font.load('Peace Sans')