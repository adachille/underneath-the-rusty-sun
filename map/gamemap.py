"""Holds data related to the game map."""
from __future__ import annotations

from typing import TYPE_CHECKING
import numpy as np
from tcod import Console

if TYPE_CHECKING:
    from engine.engine import Engine

from map import tile_types


class GameMap:
    """Holds data related to the game map."""

    def __init__(self, parent: Engine, width: int, height: int):
        self.parent = parent
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")
        self.tiles[0, :] = tile_types.wall
        self.tiles[:, 0] = tile_types.wall
        self.tiles[width - 1, :] = tile_types.wall
        self.tiles[:, height - 1] = tile_types.wall
        print(self.tiles[:5, :5])

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["graphic"]
