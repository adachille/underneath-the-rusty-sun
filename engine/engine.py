"""Class responsible for much of the rendering."""
from tcod import Console

from config import Config
from map.gamemap import GameMap
from input_handlers.base import BaseInputHandler


class Engine:
    """Class responsible for much of the rendering."""

    def __init__(self, input_handler: BaseInputHandler, console: Console):
        """Initialize."""
        self.config = Config()
        self.input_handler = input_handler
        self.console = console
        self.gamemap = GameMap(parent=self, width=console.width, height=console.height)

    def render_game(self):
        """Render game in current state."""
        self.console.clear()
        self.gamemap.render(self.console)
