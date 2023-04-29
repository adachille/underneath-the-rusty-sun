#!/usr/bin/env python3
from typing import List, Tuple
import numpy as np
import tcod

from config import Config
from colors import common_colors
from map import tile_types
from procgen.lsystem import BinaryFractalTree, TileAngle


class GameMapProcgen:
    def gen_flower(self):
        print("Gen flower")
        return None


def render_tree_tiles(
    tree_tiles: List[Tuple[int, int, TileAngle]], console: tcod.Console, char: str = "V"
):
    """Renders the tree tiles."""
    for x, y, angle in tree_tiles:
        console.print(x, y, char, fg=common_colors.bulgarian_rose)


def run_simulation():
    WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.
    config = Config("config.yml")

    tileset = tcod.tileset.load_tilesheet(
        config.paths[f'tileset_{config.view["tileset"]["name"]}'],
        config.view["tileset"]["columns"],
        config.view["tileset"]["rows"],
        tcod.tileset.CHARMAP_TCOD,
    )

    console = tcod.Console(WIDTH, HEIGHT, order="F")
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
        vsync=True,
    ) as context:
        max_steps = 5
        ms_per_step = 1000
        bft = BinaryFractalTree(max_steps, ms_per_step)
        bft.begin()
        tree_start_x, tree_start_y = 40, 50
        tree_tiles = bft.as_tiles(tree_start_x, tree_start_y)

        tiles = np.full(
            (console.width, console.height), fill_value=tile_types.floor, order="F"
        )
        print(tiles.shape)
        tiles[0, :] = tile_types.wall
        tiles[:, 0] = tile_types.wall
        tiles[console.width - 1, :] = tile_types.wall
        tiles[:, console.height - 1] = tile_types.wall

        while True:
            if bft.check_for_update():
                tree_tiles = bft.as_tiles(tree_start_x, tree_start_y)
            console.clear()
            console.rgb[0 : console.width, 0 : console.height] = tiles["graphic"]
            render_tree_tiles(tree_tiles, console)
            context.present(console)  # Show the console.
            # Needed to show console
            for event in tcod.event.wait():
                pass


if __name__ == "__main__":
    run_simulation()
