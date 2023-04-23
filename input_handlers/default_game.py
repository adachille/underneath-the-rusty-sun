"""Holds default game input handler."""
import tcod.event

from input_handlers.base import BaseInputHandler


class DefaultGameInputHandler(BaseInputHandler):
    """Holds default game input handler."""

    def handle_event(self, event: tcod.event.Event):
        """Handle game events."""
        print(event)  # Print event names and attributes.
        if isinstance(event, tcod.event.Quit):
            raise SystemExit()
