import pyglet

import gametypes

""" Global values"""
WIDTH = 800
HEIGHT = 600
BOARD_X = 200
BOARD_Y = 50
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 25

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_vsync(False)

""" load resources """
pyglet.resource.path = ['res']
pyglet.resource.reindex()
backgroundImage = pyglet.resource.image('background.png')
blocksImage = pyglet.resource.image('blocks.png')
gametypes.TetrominoType.class_init(blocksImage, BLOCK_SIZE)

""" init game state """
queue = gametypes.NextTetrominoQueue(500, 200, BLOCK_SIZE)
board = gametypes.Board(BOARD_X, BOARD_Y, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, queue)
infoDisplay = gametypes.InfoDisplay(window)
input = gametypes.Input()
game = gametypes.Game(board, infoDisplay, input, backgroundImage, queue)


@window.event
def on_key_press(symbol, modifiers):
    input.process_keypress(symbol, modifiers)


@window.event
def on_text_motion(motion):
    input.process_text_motion(motion)


@window.event
def on_draw():
    game.draw()


def update(dt):
    game.update()


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
