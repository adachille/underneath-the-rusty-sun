"""Class responsible for much of the rendering."""
from tcod import Console

from config import Config
from entities.entity import Entity
from map.gamemap import GameMap


class Engine:
    """Class responsible for much of the rendering."""

    def __init__(self, console: Console, player: Entity):
        """Initialize."""
        self.config = Config()
        self.console = console
        self.player = player
        self.gamemap = GameMap(
            width=console.width, height=console.height, player=self.player
        )

    def render_game(self):
        """Render game in current state."""
        self.console.clear()
        self.gamemap.render(self.console)
