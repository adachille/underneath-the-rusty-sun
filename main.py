#!/usr/bin/env python3
import tcod

import exceptions
from config import Config
from engine.engine import Engine
from entities import entity_factories
from input_handlers.default_input_handler import DefaultGameInputHandler

# Do something with these, make them configurable or something
WIDTH, HEIGHT = 80, 60  # Console width and height in tiles.


# TODO: add logging
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
    engine = Engine(
        console=console,
        player=entity_factories.player,
    )
    input_handler = DefaultGameInputHandler(engine=engine)
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
        vsync=True,
    ) as context:
        try:
            while True:  # Main loop, runs until SystemExit is raised.
                engine.render_game()  # Render to console
                context.present(engine.console)  # Show the console.

                for event in tcod.event.wait():
                    context.convert_event(
                        event
                    )  # Sets tile coordinates for mouse events.

                    # Kind of janky but I don't want to introduce circular dependencies
                    new_input_handler = input_handler.handle_event(event)
                    if new_input_handler is None:
                        input_handler = DefaultGameInputHandler(engine)
                    else:
                        input_handler = new_input_handler
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            # save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            # save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()
