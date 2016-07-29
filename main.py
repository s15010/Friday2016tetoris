import pyglet
import game

class Main(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width=width, height=height)
        self.width = width
        self.height = height

        # リソースパス再設定
        pyglet.resource.path = ['res']
        pyglet.resource.reindex()

        # 背景画像取得
        self.background = pyglet.resource.image('background.jpg')  # type: pyglet.image.AbstractImage
        self.image_center(self.background)

        # ゲームシステムの初期化
        game.TetrominoType.block_init(pyglet.resource.image('blocks.png'), 25)

        # テスト用のブロック TODO:あとから消す
        self.test_block = game.TetrominoType.TYPES[1]  # type: game.TetrominoType

    def on_draw(self):
        self.clear()
        self.background.blit(self.width / 2, self.height / 2)

        # テスト用ブロックの描画テスト TODO:後で消す
        for block in self.test_block.coordinates[0]:
            self.test_block.block.blit(block[0] * 25, block[1] * 25)

    @staticmethod
    def image_center(image: pyglet.image.AbstractImage):
        image.anchor_y = image.height / 2
        image.anchor_x = image.width / 2


if __name__ == '__main__':
    main = Main(width=800, height=600)
    pyglet.app.run()
