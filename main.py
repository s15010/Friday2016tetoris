import pyglet
import game

# グローバルな定数たち
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class Main(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width=width, height=height)
        self.width = width
        self.height = height
        pyglet.resource.path = ['res']
        pyglet.resource.reindex()
        self.background = pyglet.resource.image('background.jpg')  # type: pyglet.image.AbstractImage
        self.block_image = pyglet.resource.image('blocks.png')  # type: pyglet.image.AbstractImage
        self.block_size = min(self.block_image.width, self.block_image.height)

        game.TetrominoType.block_init(self.block_image, self.block_size)
        self.queue = game.NextTetrominoQueue()

        self.board = game.Board(100, 10, self.block_size, self.queue)

        # でばぐよう
        self.board.spawn_tetromino()

    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        self.board.draw()

    def update(self, delta):
        pass

    def on_key_press(self):
        pass

    def on_text_motion(self):
        pass



if __name__ == '__main__':
    main = Main(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    pyglet.app.run()
