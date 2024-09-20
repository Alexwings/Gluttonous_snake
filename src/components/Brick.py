from enum import Enum
from components.BasicBrick import Coordinates, BasicBrick

class Brick(BasicBrick):

    class Direction(Enum):
        Neutral = 0
        UP = 1
        DOWN = 1 << 1
        LEFT = 1 << 2
        RIGHT = 1 << 3

    def __init__(self, position: Coordinates, width: float = 0, height: float = 0) -> None:
        super().__init__(position, width, height)
        self.direction = Brick.Direction.Neutral

    def update_direction(self, new_direct: Direction) -> None:
        self.direction = new_direct
    
    #Equatables
    def __eq__(self, other):
        if not isinstance(other, Brick):
            return False
        origin_equal = self.origin.x == other.origin.x and self.origin.y == other.origin.y 
        size_equal = self.width == other.width and self.height == other.height
        direct_equal = self.direction == other.direction
        return origin_equal and size_equal and direct_equal
    #Equal Origin
    def pos_equal(self, other):
        if not isinstance(other, Brick):
            return False
        x_equal = self.origin.x == other.origin.x
        y_equal = self.origin.y == other.origin.y
        return x_equal and y_equal
    #Equal Shape
    def shape_equal(self, other):
        if not isinstance(other, Brick):
            return False
        return self.width == other.width and self.height == other.height

    #Equal direction
    def dir_equal(self, other):
        if not isinstance(other, Brick):
            return False
        return self.direction == other.direction