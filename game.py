import pyglet


class Board(object):
    """
    テトリスのボード部分の実装
    ボードは縦20横10マスの予定
    """

    def __init__(self):
        super().__init__()
        self.fixed_block = [[0] * 10] * 20


class TetrominoType(object):
    """
    テトロミノの種類を定義
    """

    def __init__(self, block_image, local_coordinates):
        self.block = block_image  # type: pyglet.image.AbstractImage
        self.coordinates = local_coordinates  # type: tuple

    @staticmethod
    def block_init(block_image, block_size):
        dummy = block_image.get_region(block_size * 0, 0, block_size, block_size)
        cyan = block_image.get_region(block_size * 1, 0, block_size, block_size)
        yellow = block_image.get_region(block_size * 2, 0, block_size, block_size)
        green = block_image.get_region(block_size * 3, 0, block_size, block_size)
        red = block_image.get_region(block_size * 4, 0, block_size, block_size)
        blue = block_image.get_region(block_size * 5, 0, block_size, block_size)
        orange = block_image.get_region(block_size * 6, 0, block_size, block_size)
        purple = block_image.get_region(block_size * 7, 0, block_size, block_size)

        TetrominoType.TYPES = (
            # type I
            TetrominoType(cyan,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (2, 0), (3, 0)
                              ),
                              (  # 右回り1段階
                                  (1, 0), (1, 1), (1, 2), (1, 3)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (1, 0), (2, 0), (3, 0)
                              ),
                              (  # 右回り3段階
                                  (1, 0), (1, 1), (1, 2), (1, 3)
                              ),
                          )),
            # type o
            TetrominoType(yellow,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                              (  # 右回り3段階
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                          )),
            # type s
            TetrominoType(green,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (1, 1), (2, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 2), (0, 1), (1, 1), (1, 0)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (1, 0), (1, 1), (2, 1)
                              ),
                              (  # 右回り3段階
                                  (0, 2), (0, 1), (1, 1), (1, 0)
                              ),
                          )),
            # type z
            TetrominoType(red,
                          (
                              (  # 初期の向き
                                  (0, 1), (1, 1), (1, 0), (2, 0)
                              ),
                              (  # 右回り1段階
                                  (1, 2), (1, 1), (0, 1), (0, 0)
                              ),
                              (  # 右回り2段階
                                  (0, 1), (1, 1), (1, 0), (2, 0)
                              ),
                              (  # 右回り3段階
                                  (1, 2), (1, 1), (0, 1), (0, 0)
                              ),
                          )),
            # type j
            TetrominoType(blue,
                          (
                              (  # 初期の向き
                                  (0, 1), (0, 0), (1, 0), (2, 0)
                              ),
                              (  # 右回り1段階
                                  (0, 0), (0, 1), (0, 2), (1, 2)
                              ),
                              (  # 右回り2段階
                                  (0, 1), (1, 1), (2, 1), (2, 0)
                              ),
                              (  # 右回り3段階
                                  (0, 0), (1, 0), (1, 1), (1, 2)
                              ),
                          )),
            # type L
            TetrominoType(orange,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (2, 0), (2, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 2), (0, 1), (0, 0), (1, 0)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (0, 1), (1, 1), (2, 1)
                              ),
                              (  # 右回り3段階
                                  (0, 2), (1, 2), (1, 1), (1, 0)
                              ),
                          )),
            # type t
            TetrominoType(cyan,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (2, 0), (1, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 2), (0, 1), (0, 0), (1, 1)
                              ),
                              (  # 右回り2段階
                                  (0, 1), (1, 1), (2, 1), (1, 0)
                              ),
                              (  # 右回り3段階
                                  (1, 0), (1, 1), (1, 2), (0, 1)
                              ),
                          )),
        )
