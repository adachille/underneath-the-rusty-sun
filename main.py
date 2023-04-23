#!/usr/bin/env python3
import tcod

from config import Config
from engine.engine import Engine
from input_handlers.default_game import DefaultGameInputHandler

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
    engine = Engine(input_handler=DefaultGameInputHandler(), console=console)
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
    ) as context:
        while True:  # Main loop, runs until SystemExit is raised.
            engine.render_game()  # Render to console
            context.present(engine.console)  # Show the console.

            for event in tcod.event.wait():
                context.convert_event(event)  # Sets tile coordinates for mouse events.
                engine.input_handler.handle_event(event)


if __name__ == "__main__":
    main()
