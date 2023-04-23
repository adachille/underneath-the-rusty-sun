"""Holds actions that deal with movement."""

from actions.action import Action
from entities.entity import Entity


class ActionWithMovement(Action):
    """An action that deals with movement."""

    def __init__(self, actor: Entity, dx: int, dy: int) -> None:
        super().__init__(actor)
        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        """Perform action with movement. Must be overriden by extending class."""
        raise NotImplementedError()


class MoveAction(Action):
    """An action that moves the actor."""

    def __init__(self, actor: Entity, dx: int, dy: int) -> None:
        super().__init__(actor)
        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        """Move actor."""
        self.actor.move(self.dx, self.dy)
