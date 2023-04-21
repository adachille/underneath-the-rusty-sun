#!/usr/bin/env python3
import tcod

from config import Config

WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.


def main() -> None:
    """Script entry point."""
    config = Config()

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
    ) as context:
        while True:  # Main loop, runs until SystemExit is raised.
            console.clear()
            console.print(x=0, y=0, string="Hello World!")
            context.present(console)  # Show the console.

            for event in tcod.event.wait():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                print(event)  # Print event names and attributes.
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()


if __name__ == "__main__":
    main()
