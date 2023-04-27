import tcod

from config import Config
from colors.common_colors import white
from procgen.lsystem import BinaryFractalTree


class GameMapProcgen:
    def gen_flower(self):
        print("Gen flower")
        return None


def run_simulation():
    max_steps = 5
    ms_per_step = 1000
    bft = BinaryFractalTree(max_steps, ms_per_step)
    bft.begin()
    print(bft.cur_state)
    while True:
        new_state = bft.check_for_iteration()
        if new_state is not None:
            print(new_state)
        if bft.steps_executed == max_steps:
            raise Exception
    WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.
    config = Config("config.yml")

    console = tcod.Console(WIDTH, HEIGHT)
    tileset = tcod.tileset.load_tilesheet(
        config.paths[f'tileset_{config.view["tileset"]["name"]}'],
        config.view["tileset"]["columns"],
        config.view["tileset"]["rows"],
        tcod.tileset.CHARMAP_TCOD,
    )
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
    ) as context:
        procgen = GameMapProcgen()
        print(tileset)
        for i in range(10):
            for j in range(10):
                idx = i * 10 + j
                console.print(i, j, tileset.get_tile(idx).data, fg=white)
        flower = procgen.gen_flower()
        # console.clear()
        # console.rgb[0 : width, 0 : height] = tiles["graphic"]
        #
        # console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
        context.present(console)  # Show the console.


if __name__ == "__main__":
    run_simulation()
