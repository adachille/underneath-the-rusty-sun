from typing import Tuple

import numpy as np

from colors import common_colors

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),
        ("tile_type", str),
        ("graphic", graphic_dt),
    ]  # True if this tile can be walked over.
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    tile_type: str,
    graphic_dt: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, tile_type, graphic_dt), dtype=tile_dt)


floor = new_tile(
    walkable=True,
    tile_type="Floor",
    graphic_dt=(ord(" "), (255, 255, 255), common_colors.caribbean_green),
)
wall = new_tile(
    walkable=False,
    tile_type="Wall",
    graphic_dt=(ord(" "), (255, 255, 255), common_colors.deep_jungle_green),
)
