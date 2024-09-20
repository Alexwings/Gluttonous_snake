from PyQt6.QtCore import QTimer, Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QKeyEvent, QPaintEvent, QPainter, QPen, QFont, QColor
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from components.Brick import Brick 
from components.BasicBrick import Coordinates
from components.Constants import BRICK_SIZE
from components.Snake import Snake
from components.MessageRouter import router

import queue
import random
#500 x 600

class GameBoardWidget(QWidget):
    
    score_signal = pyqtSignal(int)
    def __init__(self, width=None, height=None):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(16) #60 frames per second, so approximatly 16ms per frame
        self.timer.timeout.connect(self.update)
        self.action_queue = queue.Queue()
        self.action_flush_counter = 0
        if width is not None and height is not None:
            self.resize(width, height + 50)
        col_num = self.width() // BRICK_SIZE
        row_num = self.height() // BRICK_SIZE 
        padding = BRICK_SIZE // 2
        bricks = []
        for r in range(0, row_num - 1):
            cur_brick_row = []
            for c in range(0, col_num - 1):
                coord = Coordinates(c * BRICK_SIZE + padding, r * BRICK_SIZE + padding)
                cur_brick_row.append(Brick(coord, width=BRICK_SIZE, height=BRICK_SIZE))
            bricks.append(cur_brick_row)
        self.brick_matrics = bricks
        play_ground_width = float(col_num * BRICK_SIZE)
        play_ground_height = float(row_num * BRICK_SIZE)
        centerx = (col_num // 2 - 1) * BRICK_SIZE + padding
        centery = (row_num // 2 - 1) * BRICK_SIZE + padding
        self.snake = Snake(length=2, head=Coordinates(centerx, centery))
        self.snake.put_in_box(play_ground_width, play_ground_height)
        self.update()

#lifecycle
    def paintEvent(self, event: QPaintEvent | None) -> None:
        #处理动作
        self.flush_action()
        if self.check_bait_is_taken():
            self.snake.grow()
            self.bait = self.create_bait()
            self.score_signal.emit(self.snake.score)
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(1)
        painter.setPen(pen)
        self.render_snake(self.snake, painter)
        self.render_bait(self.bait, painter)
        return super().paintEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        if event is not None:
            if event.key() == Qt.Key.Key_Up:
                self.action_queue.put(Brick.Direction.UP)
            elif event.key() == Qt.Key.Key_Down:
                self.action_queue.put(Brick.Direction.DOWN)
            elif event.key() == Qt.Key.Key_Left:
                self.action_queue.put(Brick.Direction.LEFT)
            elif event.key() == Qt.Key.Key_Right:
                self.action_queue.put(Brick.Direction.RIGHT)
        return super().keyPressEvent(event)

    def flush_action(self):
        try: 
            action = self.action_queue.get(timeout=1)
            match action:
                case Brick.Direction.UP:
                    if self.snake.direction != Brick.Direction.DOWN:
                        self.snake.set_head_direction(action)
                case Brick.Direction.DOWN:
                    if self.snake.direction != Brick.Direction.UP:
                        self.snake.set_head_direction(action)
                case Brick.Direction.LEFT:
                    if self.snake.direction != Brick.Direction.RIGHT:
                        self.snake.set_head_direction(action)
                case Brick.Direction.RIGHT:
                    if self.snake.direction != Brick.Direction.LEFT:
                        self.snake.set_head_direction(action)
            self.action_queue.task_done()
        except queue.Empty as empty:
            pass
        if self.snake.direction != Brick.Direction.Neutral:
            try:
                self.snake.move()
            except Snake.DeadException as dead:
                self.snake.set_head_direction(Brick.Direction.Neutral)
                router.show_alert(message=f'{dead}', title="Game Over")
                self.timer.stop()


#render function
    def render_snake(self, snake: Snake, painter:QPainter):
        color = Qt.GlobalColor.cyan
        for brick in snake.body:
            pos = brick.origin
            painter.setBrush(color)
            painter.drawRect(int(pos.x), int(pos.y), int(brick.width), int(brick.height))

    def render_bait(self, bait: Brick | None, painter: QPainter):
        if bait is None:
            return
        color = Qt.GlobalColor.cyan
        painter.setBrush(color)
        painter.drawRect(int(bait.origin.x), int(bait.origin.y), int(bait.width), int(bait.height))

#Game logic
    def create_bait(self) -> Brick:
        row = random.randint(0, len(self.brick_matrics) - 1)
        col = random.randint(0, len(self.brick_matrics[0]) - 1)
        bait = self.brick_matrics[row][col]
        if self.snake.is_in_body(bait): 
            #if random number is overlapped with snake, repick one
            return self.create_bait()
        return bait
    def check_bait_is_taken(self) -> bool:
        if self.snake.head is None: return False
        if self.bait is None: return False
        return self.bait.pos_equal(self.snake.head)
#Public interface
    def start_timer(self):
        self.bait = self.create_bait()
        self.timer.start();