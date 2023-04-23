"""Define base entity class."""
from typing import Tuple


class Entity:
    """Base entity class."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
