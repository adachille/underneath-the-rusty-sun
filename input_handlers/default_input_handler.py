"""Holds default game input handler."""
from typing import Optional

import tcod.event

from actions.action import Action
from actions.move_actions import MoveAction
from engine.engine import Engine
from input_handlers.base_input_handler import BaseInputHandler, MOVE_KEYS, WAIT_KEYS


class DefaultGameInputHandler(BaseInputHandler):
    """Holds default game input handler."""

    def __init__(self, engine: Engine):
        super().__init__(engine)

    def ev_keydown(self, event: tcod.event.Event) -> Optional[Action]:
        """Handle game events."""
        action: Optional[Action] = None
        print(event)  # Print event names and attributes.

        key = event.sym
        modifier = event.mod
        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = MoveAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = MoveAction(player, 0, 0)

        if isinstance(event, tcod.event.Quit):
            raise SystemExit()

        return action
