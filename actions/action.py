"""Holds a class representing all actions taken by agents."""


class Action:
    """Class representing all actions taken by agents."""

    def __init__(self) -> None:
        super().__init__()

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()
