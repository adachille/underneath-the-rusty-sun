"""Holds data related to the game map."""
import numpy as np
from tcod import Console

from entities.entity import Entity
from map import tile_types


class GameMap:
    """Holds data related to the game map."""

    def __init__(self, width: int, height: int, player: Entity):
        self.width, self.height = width, height
        self.tiles = self.init_tiles(width, height)
        self.entities = {player}
        self.player = player

    def init_tiles(self, width, height):
        """Temporary function until we have procgen."""
        tiles = np.full((height, width), fill_value=tile_types.floor)
        tiles[0, :] = tile_types.wall
        tiles[:, 0] = tile_types.wall
        tiles[width - 1, :] = tile_types.wall
        tiles[:, height - 1] = tile_types.wall
        return tiles

    def render(self, console: Console) -> None:
        """Renders the map."""
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["graphic"]

        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
