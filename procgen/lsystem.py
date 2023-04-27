"""A class representing an LSystem for fractal generation."""
import time

from typing import List, Optional


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
        max_steps: the maximum number of steps
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
        self.time_of_last_iteration: int = None

    def begin(self) -> None:
        """Begin Lsystem iterations."""
        self.time_of_last_iteration = self.get_cur_time_ms()

    def check_for_iteration(self) -> Optional[str]:
        """Check if iteration should be executed, if so, return next step."""
        if self.steps_executed >= self.max_steps:
            return None

        cur_time = self.get_cur_time_ms()
        if self.time_of_last_iteration is None:
            self.time_of_last_iteration = cur_time
            return None

        if self.time_of_last_iteration + self.ms_per_step <= cur_time:
            self.time_of_last_iteration = cur_time
            self.iterate()
            return self.cur_state
        return None

    def iterate(self) -> None:
        """Iterate on state."""
        self.steps_executed += 1
        self.cur_state = "".join(
            [
                self.rules[char] if char in self.rules else char
                for char in self.cur_state
            ]
        )

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
        rules = {"1": "11", "0": "1[0][0]"}
        super().__init__(variables, constants, axiom, rules, max_steps, ms_per_step)
