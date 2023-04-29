"""A class representing an LSystem for fractal generation."""
import time
from enum import Enum
from typing import List, Tuple


class TileAngle(Enum):
    """Represents a tile angle."""

    UP = 0
    UP_LEFT = 1
    LEFT = 2
    DOWN_LEFT = 3
    DOWN = 4
    DOWN_RIGHT = 5
    RIGHT = 6
    UP_RIGHT = 7


TILE_ANGLE_TO_D_POS = {
    TileAngle.UP: (0, -1),
    TileAngle.UP_LEFT: (-1, -1),
    TileAngle.LEFT: (-1, 0),
    TileAngle.DOWN_LEFT: (-1, 1),
    TileAngle.DOWN: (0, 1),
    TileAngle.DOWN_RIGHT: (1, 1),
    TileAngle.RIGHT: (1, 0),
    TileAngle.UP_RIGHT: (1, -1),
}


class LSystem:
    """A class representing an LSystem for fractal generation."""

    def __init__(
        self,
        variables: List[str],
        constants: List[str],
        axiom: str,
        rules: dict,
        max_steps: int = 5,
        ms_per_step: float = 2000,
    ):
        """Create an LSystem.

        variables: a list of all variables (replaceable states) in alphabet
        constants: a list of all constants (terminal states) in alphabet
        axiom: start state
        rules: a dict of rules that dictates how variables can be replaced
        max_steps: the maximum number of steps to simulate
        ms_per_step: number of milliseconds between each update
        """
        self.alphabet = variables + constants
        assert all([var in self.alphabet for var in axiom])
        self.variables = variables
        self.constants = constants
        self.axiom = axiom
        self.rules = rules

        self.cur_state = self.axiom

        self.max_steps = max_steps
        self.ms_per_step = ms_per_step
        self.steps_executed = 0
        self.time_of_last_update: int = None

    def begin(self) -> None:
        """Begin Lsystem updates."""
        self.time_of_last_update = self.get_cur_time_ms()

    def check_for_update(self) -> bool:
        """Check if update should be executed, if so, return next step."""
        if self.steps_executed >= self.max_steps:
            return False

        cur_time = self.get_cur_time_ms()
        if self.time_of_last_update is None:
            self.time_of_last_update = cur_time
            return False

        if self.time_of_last_update + self.ms_per_step <= cur_time:
            self.time_of_last_update = cur_time
            self.update()
            return True
        return False

    def update(self) -> None:
        """Update on state."""
        self.steps_executed += 1
        self.cur_state = "".join(
            [
                self.rules[char] if char in self.rules else char
                for char in self.cur_state
            ]
        )

    def as_tiles(
        self, start_x: int, start_y: int, start_angle: TileAngle
    ) -> List[Tuple[int, int, TileAngle]]:
        """Convert lsytem state to tiles"""
        raise NotImplementedError

    @staticmethod
    def get_cur_time_ms() -> int:
        """Get current time in ms."""
        return time.time_ns() // 1_000_000


class BinaryFractalTree(LSystem):
    """A binary fractal tree LSystem."""

    def __init__(self, max_steps: int = 8, ms_per_step: float = 2000):
        """Create a binary fractal tree."""
        variables = ["0", "1"]
        constants = ["[", "]"]
        axiom = "0"
        rules = {"1": "11", "0": "1[0]0"}
        super().__init__(variables, constants, axiom, rules, max_steps, ms_per_step)

    def as_tiles(
        self, start_x: int, start_y: int, start_angle: TileAngle = TileAngle.UP
    ) -> List[Tuple[int, int, TileAngle]]:
        """Convert binary fractal tree to tiles."""
        cur_x, cur_y = start_x, start_y
        cur_angle = start_angle
        tiles = []
        stack = []
        for char in self.cur_state:
            if char == "0" or char == "1":
                dx, dy = TILE_ANGLE_TO_D_POS[cur_angle]
                cur_x += dx
                cur_y += dy
                tiles.append((cur_x, cur_y, cur_angle))
            elif char == "[":
                stack.append((cur_x, cur_y, cur_angle))
                cur_angle = TileAngle((cur_angle.value + 1) % 8)
                # if cur_angle == TileAngle.UP_RIGHT:
                #     cur_angle = TileAngle.UP
                # else:
                #     cur_angle += 1
            elif char == "]":
                cur_x, cur_y, cur_angle = stack.pop()
                cur_angle = TileAngle((cur_angle.value - 1) % 8)
                # if cur_angle == TileAngle.UP:
                #     cur_angle = TileAngle.UP_RIGHT
                # else:
                #     cur_angle -= 1
            else:
                raise ValueError(f"Unexpected bft value {char}")
        return tiles
