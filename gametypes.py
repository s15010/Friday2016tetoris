"""
Pygletを使ったテトリス。実装部分


"""
import random
import warnings
from collections import deque

import pyglet


class TetrominoType(object):
    TYPES = tuple()

    def __init__(self, block_image, local_coords):
        self._block_image = block_image
        self._local_coords = local_coords

    @staticmethod
    def class_init(block_image, block_size):
        """
        block_imageからblock_sizeで8色のブロックを切り出す。
        その後、7種のテトロミノタイプを定義してstaticメンバとして生成
        :param block_image: ブロック画像
        :param block_size: ブロックのサイズ
        :return: None
        """
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
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (2, 1), (3, 1)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (1, 2), (1, 3)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (2, 1), (3, 1)),
                              Tetromino.UP: ((1, 0), (1, 1), (1, 2), (1, 3)),
                          }
                          ),
            # type O
            TetrominoType(yellow,
                          {
                              Tetromino.RIGHT: ((1, 0), (1, 1), (2, 0), (2, 1)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (2, 0), (2, 1)),
                              Tetromino.LEFT: ((1, 0), (1, 1), (2, 0), (2, 1)),
                              Tetromino.UP: ((1, 0), (1, 1), (2, 0), (2, 1)),
                          }
                          ),
            # type S
            TetrominoType(green,
                          {
                              Tetromino.RIGHT: ((0, 0), (1, 0), (1, 1), (2, 1)),
                              Tetromino.DOWN: ((0, 2), (0, 1), (1, 1), (1, 0)),
                              Tetromino.LEFT: ((0, 0), (1, 0), (1, 1), (2, 1)),
                              Tetromino.UP: ((0, 2), (0, 1), (1, 1), (1, 0)),
                          }
                          ),
            # type Z
            TetrominoType(red,
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (1, 0), (2, 0)),
                              Tetromino.DOWN: ((0, 0), (0, 1), (1, 1), (1, 2)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (1, 0), (2, 0)),
                              Tetromino.UP: ((0, 0), (0, 1), (1, 1), (1, 2)),
                          }
                          ),
            # type J
            TetrominoType(blue,
                          {
                              Tetromino.RIGHT: ((0, 2), (0, 1), (1, 1), (2, 1)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (1, 2), (2, 2)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (2, 1), (2, 0)),
                              Tetromino.UP: ((0, 0), (1, 0), (1, 1), (1, 2)),
                          }
                          ),
            # type L
            TetrominoType(orange,
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (2, 1), (2, 2)),
                              Tetromino.DOWN: ((1, 2), (1, 1), (1, 0), (2, 0)),
                              Tetromino.LEFT: ((0, 0), (0, 1), (1, 1), (2, 1)),
                              Tetromino.UP: ((0, 2), (1, 2), (1, 1), (1, 0)),
                          }

                          ),
            # type T
            TetrominoType(purple,
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (2, 1), (1, 2)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (1, 2), (2, 1)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (2, 1), (1, 0)),
                              Tetromino.UP: ((1, 0), (1, 1), (1, 2), (0, 1)),
                          }
                          ),
        )

    @staticmethod
    def random_type():
        warnings.warn("キューを使う方式に変更して下さい", category=DeprecationWarning, stacklevel=2)
        return random.choice(TetrominoType.TYPES)

    def get_local_coords(self, orientation):
        return self._local_coords[orientation]

    def get_block(self):
        return self._block_image


class Tetromino(object):
    RIGHT, DOWN, LEFT, UP = range(4)
    CLOCKWISE_ROTATIONS = {RIGHT: DOWN, DOWN: LEFT, LEFT: UP, UP: RIGHT}

    def __init__(self, type=None):
        self._x = 0
        self._y = 0
        if type is None:
            self._tetromino_type = TetrominoType.random_type()  # type: TetrominoType
        else:
            self._tetromino_type = type
        self._orientation = Tetromino.RIGHT
        self._block_board_coords = self.calc_block_board_coords()

    def calc_block_board_coords(self):
        local_block_coords = self._tetromino_type.get_local_coords(self._orientation)
        grid_coords = []
        for coord in local_block_coords:
            grid_coord = (coord[0] + self._x, coord[1] + self._y)
            grid_coords.append(grid_coord)
        return grid_coords

    def get_block_board_coords(self):
        return self._block_board_coords

    def set_position(self, x, y):
        self._x = x
        self._y = y
        self._block_board_coords = self.calc_block_board_coords()

    def move_down(self):
        self._y -= 1
        self._block_board_coords = self.calc_block_board_coords()

    def move_up(self):
        self._y += 1
        self._block_board_coords = self.calc_block_board_coords()

    def move_left(self):
        self._x -= 1
        self._block_board_coords = self.calc_block_board_coords()

    def move_right(self):
        self._x += 1
        self._block_board_coords = self.calc_block_board_coords()

    def rotate_clockwise(self):
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._block_board_coords = self.calc_block_board_coords()

    def rotate_counterclockwise(self):
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._block_board_coords = self.calc_block_board_coords()

    def command(self, command):
        if command == InputProcessor.MOVE_DOWN:
            self.move_down()
        elif command == InputProcessor.MOVE_RIGHT:
            self.move_right()
        elif command == InputProcessor.MOVE_LEFT:
            self.move_left()
        elif command == InputProcessor.ROTATE_CLOCKWISE:
            self.rotate_clockwise()

    def undo_command(self, command):
        if command == InputProcessor.MOVE_DOWN:
            self.move_up()
        elif command == InputProcessor.MOVE_RIGHT:
            self.move_left()
        elif command == InputProcessor.MOVE_LEFT:
            self.move_right()
        elif command == InputProcessor.ROTATE_CLOCKWISE:
            self.rotate_counterclockwise()

    def clear_row_and_adjust_down(self, board_grid_row):
        new_block_board_coords = []
        for coord in self._block_board_coords:
            if coord[1] > board_grid_row:
                adjusted_coord = (coord[0], coord[1] - 1)
                new_block_board_coords.append(adjusted_coord)
            if coord[1] < board_grid_row:
                new_block_board_coords.append(coord)
        self._block_board_coords = new_block_board_coords
        return len(self._block_board_coords) > 0

    def draw(self, screen_coords):
        image = self._tetromino_type.get_block()
        for coords in screen_coords:
            image.blit(coords[0], coords[1])


class Board(object):
    STARTING_ZONE_HEIGHT = 4

    def __init__(self, x, y, grid_width, grid_height, block_size, queue):
        self._x = x
        self._y = y
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._block_size = block_size
        self._spawn_x = int(grid_width * 1 / 3)
        self._spawn_y = grid_height
        self._queue = queue
        self._falling_tetromino = None
        self.spawn_tetromino()
        self._tetromino_list = []

    def spawn_tetromino(self):
        self._falling_tetromino = self._queue.next()
        self._falling_tetromino.set_position(self._spawn_x, self._spawn_y)

    def command_falling_tetromino(self, command):
        self._falling_tetromino.command(command)
        if not self.is_valid_position():
            self._falling_tetromino.undo_command(command)

    def is_valid_position(self):
        non_falling_block_coords = []
        for tetromino in self._tetromino_list:
            non_falling_block_coords.extend(tetromino.get_block_board_coords())
        for coord in self._falling_tetromino.get_block_board_coords():
            out_of_bounds = coord[0] < 0 or coord[0] >= self._grid_width or \
                            coord[1] < 0
            overlapping = coord in non_falling_block_coords
            if out_of_bounds or overlapping:
                return False
        return True

    def find_full_rows(self):
        non_falling_block_coords = []
        for tetromino in self._tetromino_list:
            non_falling_block_coords.extend(tetromino.get_block_board_coords())

        row_counts = {}
        for i in range(self._grid_height + Board.STARTING_ZONE_HEIGHT):
            row_counts[i] = 0
        for coord in non_falling_block_coords:
            row_counts[coord[1]] += 1

        full_rows = []
        for row in row_counts:
            if row_counts[row] == self._grid_width:
                full_rows.append(row)
        return full_rows

    def clear_row(self, grid_row):
        tetrominos = []
        for tetromino in self._tetromino_list:
            if tetromino.clear_row_and_adjust_down(grid_row):
                tetrominos.append(tetromino)
        self._tetromino_list = tetrominos

    def clear_rows(self, grid_rows):
        grid_rows.sort(reverse=True)
        for row in grid_rows:
            self.clear_row(row)

    def update_tick(self):
        num_cleared_rows = 0
        game_lost = False
        self._falling_tetromino.command(InputProcessor.MOVE_DOWN)
        if not self.is_valid_position():
            self._falling_tetromino.undo_command(InputProcessor.MOVE_DOWN)
            self._tetromino_list.append(self._falling_tetromino)
            full_rows = self.find_full_rows()
            self.clear_rows(full_rows)
            game_lost = self.is_in_start_zone(self._falling_tetromino)
            if not game_lost:
                self.spawn_tetromino()
            num_cleared_rows = len(full_rows)
        return num_cleared_rows, game_lost

    def is_in_start_zone(self, tetromino):
        for coords in tetromino.get_block_board_coords():
            if coords[1] >= self._grid_height:
                return True
        return False

    def grid_coords_to_screen_coords(self, coords):
        screen_coords = []
        for coord in coords:
            coord = (self._x + coord[0] * self._block_size,
                     self._y + coord[1] * self._block_size)
            screen_coords.append(coord)
        return screen_coords

    def draw(self):
        for tetromino in self._tetromino_list:
            screen_coords = self.grid_coords_to_screen_coords(
                tetromino.get_block_board_coords())
            tetromino.draw(screen_coords)

        screen_coords = self.grid_coords_to_screen_coords(
            self._falling_tetromino.get_block_board_coords())
        self._falling_tetromino.draw(screen_coords)


class InfoDisplay(object):
    ROWS_CLEARED_X = 70
    ROWS_CLEARED_Y = 550

    def __init__(self, window):
        self.rowsClearedLabel = pyglet.text.Label('Rows cleared: 0',
                                                  font_size=14,
                                                  x=InfoDisplay.ROWS_CLEARED_X,
                                                  y=InfoDisplay.ROWS_CLEARED_Y
                                                  )
        self.pausedLabel = pyglet.text.Label('PAUSED',
                                             font_size=32,
                                             x=window.width // 2,
                                             y=window.height // 2,
                                             anchor_x='center',
                                             anchor_y='center'
                                             )
        self.gameoverLabel = pyglet.text.Label('GAME OVER',
                                               font_size=32,
                                               x=window.width // 2,
                                               y=window.height // 2,
                                               anchor_x='center',
                                               anchor_y='center'
                                               )
        self.showPausedLabel = False
        self.showGameoverLabel = False

    def set_rows_cleared(self, num_rows_cleared):
        self.rowsClearedLabel.text = 'Rows cleared: ' + str(num_rows_cleared)

    def draw(self):
        self.rowsClearedLabel.draw()
        if self.showPausedLabel:
            self.pausedLabel.draw()
        if self.showGameoverLabel:
            self.gameoverLabel.draw()


class InputProcessor(object):
    TOGGLE_PAUSE, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, ROTATE_CLOCKWISE = range(5)

    def __init__(self):
        self.action = None

    def process_keypress(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.action = InputProcessor.TOGGLE_PAUSE

    def process_text_motion(self, motion):
        if motion == pyglet.window.key.MOTION_LEFT:
            self.action = InputProcessor.MOVE_LEFT
        elif motion == pyglet.window.key.MOTION_RIGHT:
            self.action = InputProcessor.MOVE_RIGHT
        elif motion == pyglet.window.key.MOTION_UP:
            self.action = InputProcessor.ROTATE_CLOCKWISE
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.action = InputProcessor.MOVE_DOWN

    def consume(self):
        action = self.action
        self.action = None
        return action


class GameTick(object):
    def __init__(self, tick_on_first_call=False):
        self.tick = tick_on_first_call
        self.started = tick_on_first_call

    def is_tick(self, next_tick_time):
        def set_tick(dt):
            self.tick = True

        if not self.started:
            self.started = True
            pyglet.clock.schedule_once(set_tick, next_tick_time)
            return False
        elif self.tick:
            self.tick = False
            pyglet.clock.schedule_once(set_tick, next_tick_time)
            return True
        else:
            return False


class Game(object):
    def __init__(self, board, info_display, key_input, background_image, queue):
        self._queue = queue
        self.board = board
        self.infoDisplay = info_display
        self.input = key_input
        self.backgroundImage = background_image
        self.paused = False
        self.lost = False
        self.numRowsCleared = 0
        self.tickSpeed = 0.6
        self.ticker = GameTick()

    def add_rows_cleared(self, rows_cleared):
        self.numRowsCleared += rows_cleared
        self.infoDisplay.set_rows_cleared(self.numRowsCleared)

    def toggle_pause(self):
        self.paused = not self.paused
        self.infoDisplay.showPausedLabel = self.paused

    def update(self):
        if self.lost:
            self.infoDisplay.showGameoverLabel = True
        else:
            command = self.input.consume()
            if command == InputProcessor.TOGGLE_PAUSE:
                self.toggle_pause()
            if not self.paused:
                if command and command != InputProcessor.TOGGLE_PAUSE:
                    self.board.command_falling_tetromino(command)
                if self.ticker.is_tick(self.tickSpeed):
                    rows_cleared, self.lost = self.board.update_tick()
                    self.add_rows_cleared(rows_cleared)

    def draw(self):
        self.backgroundImage.blit(0, 0)
        self.board.draw()
        self._queue.draw()
        self.infoDisplay.draw()


class NextTetrominoQueue(object):
    """
    Nextブロックを管理するキュー
    """
    NEXT_COUNT = 3

    def __init__(self, x, y, block_size, set_count=3):
        self._x = x
        self._y = y
        self._set_count = set_count
        self._block_size = block_size
        self._queue = deque()  # type: deque
        self.generate_tetromino()

    def generate_tetromino(self):
        """
        Tetrominoをset_countセット作ってシャッフルしてキューにぶち込む
        """
        tetromino_type_set = list(TetrominoType.TYPES[:] * self._set_count)
        for a in range(3):
            random.shuffle(tetromino_type_set)

        for tetromino_type in tetromino_type_set:
            self._queue.append(Tetromino(tetromino_type))

    def get(self, index):
        return self._queue[index]  # type: Tetromino

    def next(self):
        if len(self._queue) < 5:
            self.generate_tetromino()

        return self._queue.popleft()  # type: Tetromino

    def grid_coords_to_screen_coords(self, coords):
        screen_coords = []
        for coord in coords:
            coord = (self._x + coord[0] * self._block_size,
                     self._y + coord[1] * self._block_size)
            screen_coords.append(coord)
        return screen_coords

    def draw(self):
        for i in range(self.NEXT_COUNT):
            self._queue[i].set_position(0, 4 * (self.NEXT_COUNT - i - 1))
            screen_coords = self.grid_coords_to_screen_coords(
                self._queue[i].get_block_board_coords())
            self._queue[i].draw(screen_coords)
