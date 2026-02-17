"""Direction module for maze wall configurations."""

from enum import Enum


class Direction(Enum):
    """Represents wall configuration of a maze cell.

    Each value is a 4-bit hex number where bits represent:
    - bit 0: North wall (1 = closed, 0 = open)
    - bit 1: East wall
    - bit 2: South wall
    - bit 3: West wall
    """
    OPENED = int("0", 16)
    ESW = int("1", 16)
    NSW = int("2", 16)
    SW = int("3", 16)
    NEW = int("4", 16)
    EW = int("5", 16)
    NW = int("6", 16)
    W = int("7", 16)
    NES = int("8", 16)
    ES = int("9", 16)
    NS = int("A", 16)
    S = int("B", 16)
    NE = int("C", 16)
    E = int("D", 16)
    N = int("E", 16)
    CLOSED = int("F", 16)

    def can_see(self, cardinal_point: 'Direction') -> bool:
        """Check if there's no wall in the given direction.

        Args:
            cardinal_point: Direction to check (N, E, S, or W).

        Returns:
            True if the wall is open in that direction.
        """
        if cardinal_point.value == Direction.S.value:
            return self.value in (
                Direction.OPENED.value,
                Direction.S.value,
                Direction.SW.value,
                Direction.ES.value,
                Direction.NES.value,
                Direction.NSW.value,
                Direction.NS.value,
                Direction.ESW.value
            )
        elif cardinal_point.value == Direction.N.value:
            return self.value in (
                Direction.OPENED.value,
                Direction.NES.value,
                Direction.NEW.value,
                Direction.NE.value,
                Direction.NSW.value,
                Direction.NS.value,
                Direction.NW.value,
                Direction.N.value
            )
        elif cardinal_point.value == Direction.E.value:
            return self.value in (
                Direction.OPENED.value,
                Direction.NES.value,
                Direction.NEW.value,
                Direction.NE.value,
                Direction.ESW.value,
                Direction.ES.value,
                Direction.EW.value,
                Direction.E.value
            )
        elif cardinal_point.value == Direction.W.value:
            return self.value in (
                Direction.OPENED.value,
                Direction.NEW.value,
                Direction.NSW.value,
                Direction.NW.value,
                Direction.ESW.value,
                Direction.EW.value,
                Direction.SW.value,
                Direction.W.value
            )

        return False
