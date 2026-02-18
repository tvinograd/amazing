"""Cell module representing a single maze cell."""

from mazegen.direction import Direction


class Cell:
    """A single cell in the maze grid."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell.

        Args:
            x: X coordinate of the cell.
            y: Y coordinate of the cell.
        """
        self.coordinate = (x, y)
        self.is_visited = False
        self.direction = Direction.CLOSED
