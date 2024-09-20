from components.Brick import Brick
from components.BasicBrick import Coordinates
from typing import List
from components.Constants import BOX_WIDTH, BOX_HEIGHT, BRICK_SIZE

from PyQt6.QtCore import pyqtSignal


class Snake:
    class DeadException(Exception):
        @classmethod
        def eat_self(cls, body: List[Brick]):
            if len(body) <= 0: return None
            head = body[0]
            for block in body[1:]:
                if head.pos_equal(block):
                    return Snake.DeadException('You ate yourself!')
            return None

        @classmethod
        def out_of_box(cls, width: float, height: float, head: Brick):
            # 宽度为None 表示左右无限制
            if width is None and head.direction == Brick.Direction.LEFT or head.direction == Brick.Direction.RIGHT:
                return None
            if height is None and head.direction == Brick.Direction.UP or head.direction == Brick.Direction.DOWN:
                return None
            if head.origin.x < 0 or head.origin.y < 0:
                return Snake.DeadException('Hit the box boundry!')
            if head.direction == Brick.Direction.RIGHT and head.origin.x > width:
                return Snake.DeadException('Hit the box boundry!')
            if head.direction == Brick.Direction.RIGHT and head.origin.x > width:
                return Snake.DeadException('Hit the box boundry!')

    def __init__(self, size:int = BRICK_SIZE, length = 1, head: Coordinates = Coordinates(0,0)) -> None:
        self.length = length
        body: List[Brick] = []
        self.size = size
        cur_coord = head
        for i in range(0,length):
            body_block = Brick(cur_coord, size, size)
            body_block.update_direction(Brick.Direction.UP)
            body.append(body_block)
            cur_coord = Coordinates(head.x, head.y + size * (i + 1))
        self.body = body
        self.initial_length = length

    @classmethod
    def create_in_box(cls, width: float, height:float):
        center = Coordinates(BOX_WIDTH // 2, BOX_HEIGHT // 2)
        player = Snake(head=center)
        player.put_in_box(width, height)
        return player

    @property
    def direction(self) -> Brick.Direction:
        if self.body is None:
            return Brick.Direction.Neutral
        return self.body[0].direction
    
    @property
    def head(self) -> Brick | None:
        return self.body[0] if len(self.body) > 0 else None

    @property
    def score(self) -> int:
        if self.body is None:
            return 0
        if len(self.body) < self.initial_length:
            return 0
        return len(self.body) - self.initial_length
    
    #Put the snake inside a box boundray
    def put_in_box(self, width, height):
        self.box_width = width
        self.box_height = height
    
    def is_in_body(self, brick: Brick) -> bool:
        if self.body is None:
            return False
        result = [item for item in self.body if item.pos_equal(brick)]
        return len(result) > 0

    def set_head_direction(self, direct=Brick.Direction):
        if self.body is None:
            return
        self.body[0].update_direction(direct)

    def update_all_direction(self):
        prev_direct = self.body[0].direction
        for block in self.body:
            cur_direct = block.direction
            block.update_direction(prev_direct)
            prev_direct = cur_direct
    
    def move(self,step = 1):
        if self.body is None:
            return
        delta = step * self.size
        for block in self.body:
            match block.direction:
                case Brick.Direction.UP:
                    block.move(block.origin.x, block.origin.y - delta)
                case Brick.Direction.DOWN:
                    block.move(block.origin.x, block.origin.y + delta)
                case Brick.Direction.LEFT:
                    block.move(block.origin.x - delta, block.origin.y)
                case Brick.Direction.RIGHT:
                    block.move(block.origin.x + delta, block.origin.y)
        self.update_all_direction()
        exception = Snake.DeadException.eat_self(self.body)
        if exception is not None:
            raise exception
        exception = Snake.DeadException.out_of_box(width=self.box_width, height=self.box_height, head=self.body[0])
        if exception is not None:
            raise exception
    
    def grow(self):
        tail = self.body[-1]
        new_x = tail.origin.x
        new_y = tail.origin.y
        if tail.direction == Brick.Direction.UP:
            new_y += self.size
        elif tail.direction == Brick.Direction.DOWN:
            new_y -= self.size
        elif tail.direction == Brick.Direction.LEFT:
            new_x += self.size
        elif tail.direction == Brick.Direction.RIGHT:
            new_x -= self.size
        pos = Coordinates(new_x, new_y)
        new_tail = Brick(pos, self.size, self.size)
        new_tail.update_direction(tail.direction)
        self.body.append(new_tail)

    