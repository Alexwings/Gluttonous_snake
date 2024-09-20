from abc import ABC, abstractmethod
from typing import NamedTuple

class Coordinates(NamedTuple):
    x: float
    y: float

class BasicBrick(ABC):

    def __init__(self, position:Coordinates, width:float=0, height:float=0) -> None:
        self.pos = position
        self.width = width
        self.height = height
    
    @property
    def max_X(self) -> None:
        return self.pos.x + self.width
    
    @property
    def max_Y(self) -> None:
        return self.pos.y + self.height
    
    @property
    def center(self) -> Coordinates:
        midX = self.pos.x + self.width / 2
        midY = self.pos.x + self.height / 2
        return  Coordinates(midX, midY)
    
    @property
    def origin(self) -> Coordinates:
        return self.pos
    
    def move(self, x: float, y: float) -> None:
        self.pos = Coordinates(x, y)
    
    def move_to_center(self, new_location:Coordinates) -> None:
        new_x = new_location.x - self.width / 2.0
        new_y = new_location.y - self.height / 2.0
        self.pos = Coordinates(new_x, new_y)