#!/usr/bin/env python3
from typing import List, Tuple
import numpy as np
import tcod

from config import Config
from colors import common_colors
from enum import Enum
from map import tile_types
from procgen.lsystem import BinaryFractalTree


class GameMapProcgen:
    def gen_flower(self):
        print("Gen flower")
        return None


# Move to lsytem
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


# TODO: move this to lsystem
def convert_binary_fractal_tree(
    bft_state: str, start_x: int, start_y: int, start_angle: TileAngle = TileAngle.UP
):
    """Convert binary fractal tree to tiles"""
    cur_x, cur_y = start_x, start_y
    cur_angle = start_angle
    tiles = []
    stack = []
    for char in bft_state:
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
        tree_tiles = convert_binary_fractal_tree(
            bft.cur_state, tree_start_x, tree_start_y
        )

        tiles = np.full(
            (console.width, console.height), fill_value=tile_types.floor, order="F"
        )
        print(tiles.shape)
        tiles[0, :] = tile_types.wall
        tiles[:, 0] = tile_types.wall
        tiles[console.width - 1, :] = tile_types.wall
        tiles[:, console.height - 1] = tile_types.wall

        while True:
            new_state = bft.check_for_update()
            if new_state is not None:
                tree_tiles = convert_binary_fractal_tree(
                    bft.cur_state, tree_start_x, tree_start_y
                )
            console.clear()
            console.rgb[0 : console.width, 0 : console.height] = tiles["graphic"]
            render_tree_tiles(tree_tiles, console)
            context.present(console)  # Show the console.
            # Needed to show console
            for event in tcod.event.wait():
                pass


if __name__ == "__main__":
    run_simulation()
