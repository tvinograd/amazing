"""Canvas module for maze grid management."""

from models.cell import Cell
from models.direction import Direction


class Canvas():
    """Represents the maze grid with cells and wall management."""

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int]
    ) -> None:
        """Initialize the canvas.

        Args:
            width: Width of the maze in cells.
            height: Height of the maze in cells.
            entry: Entry coordinates (x, y).
            exit: Exit coordinates (x, y).
        """
        self.width: int = width
        self.height: int = height
        self.cells: list[Cell] = []
        self.ft_cells: list[Cell] = []
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.dead_ends: list[tuple[Cell, Cell]] = []

        for x in range(width):
            for y in range(height):
                self.cells.append(Cell(x, y))

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at coordinates.

        Args:
            x: X coordinate.
            y: Y coordinate.

        Returns:
            Cell at coordinates or None if not found.
        """
        for cell in self.cells:
            if cell.coordinate == (x, y):
                return cell
        return None

    def get_neighbours(self, cell: Cell) -> list[Cell]:
        """Get all neighbouring cells.

        Args:
            cell: The cell to get neighbours for.

        Returns:
            List of neighbouring cells.
        """
        neighbours: list[Cell | None] = []
        if cell:
            x = cell.coordinate[0]
            y = cell.coordinate[1]

            if x - 1 >= 0:
                neighbours.append(self.get_cell(x-1, y))
            if x + 1 < self.width:
                neighbours.append(self.get_cell(x+1, y))
            if y - 1 >= 0:
                neighbours.append(self.get_cell(x, y-1))
            if y + 1 < self.height:
                neighbours.append(self.get_cell(x, y+1))

        return [n for n in neighbours if n]

    def get_accessible_neighbours(self, cell: Cell) -> list[Cell]:
        """Get neighbours accessible through open walls.

        Args:
            cell: The cell to check from.

        Returns:
            List of accessible neighbouring cells.
        """
        accessible: list[Cell] = []
        x, y = cell.coordinate

        for neighbour in self.get_neighbours(cell):
            nx, ny = neighbour.coordinate

            # Neighbour is NORTH of cell
            if ny == y - 1:
                if (neighbour.direction.can_see(Direction.S)
                        and cell.direction.can_see(Direction.N)):
                    accessible.append(neighbour)

            # Neighbour is SOUTH of cell
            elif ny == y + 1:
                if (neighbour.direction.can_see(Direction.N)
                        and cell.direction.can_see(Direction.S)):
                    accessible.append(neighbour)

            # Neighbour is WEST of cell
            elif nx == x - 1:
                if (neighbour.direction.can_see(Direction.E)
                        and cell.direction.can_see(Direction.W)):
                    accessible.append(neighbour)

            # Neighbour is EAST of cell
            elif nx == x + 1:
                if (neighbour.direction.can_see(Direction.W)
                        and cell.direction.can_see(Direction.E)):
                    accessible.append(neighbour)

        return accessible

    def remove_wall(self, cell: Cell, neighbour: Cell) -> None:
        """Remove wall between two neighbouring cells.

        Args:
            cell: First cell.
            neighbour: Neighbouring cell to remove wall to.
        """
        if neighbour in self.ft_cells:
            return

        x, y = cell.coordinate[0], cell.coordinate[1]

        # Neighbour is WEST of cell
        if neighbour.coordinate == (x-1, y):
            if cell.direction.value & 8:
                cell.direction = Direction(cell.direction.value - 8)
            if neighbour.direction.value & 2:
                neighbour.direction = Direction(neighbour.direction.value - 2)

        # Neighbour is NORTH of cell
        elif neighbour.coordinate == (x, y-1):
            if cell.direction.value & 1:
                cell.direction = Direction(cell.direction.value - 1)
            if neighbour.direction.value & 4:
                neighbour.direction = Direction(neighbour.direction.value - 4)

        # Neighbour is EAST of cell
        elif neighbour.coordinate == (x+1, y):
            if cell.direction.value & 2:
                cell.direction = Direction(cell.direction.value - 2)
            if neighbour.direction.value & 8:
                neighbour.direction = Direction(neighbour.direction.value - 8)

        # Neighbour is SOUTH of cell
        elif neighbour.coordinate == (x, y+1):
            if cell.direction.value & 4:
                cell.direction = Direction(cell.direction.value - 4)
            if neighbour.direction.value & 1:
                neighbour.direction = Direction(neighbour.direction.value - 1)
