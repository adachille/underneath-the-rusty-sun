"""Holds base input handler that all others extend."""
from typing import Union

import tcod.event

from actions.action import Action

ActionOrHandler = Union[Action, "BaseEventHandler"]


class BaseInputHandler(tcod.event.EventDispatch[ActionOrHandler]):
    """Base input handler that all others extend."""

    def handle_event(self, event: tcod.event.Event):
        raise NotImplementedError
