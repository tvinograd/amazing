"""Maze generator module with generation, solving and rendering."""

import random
import sys
import time
from collections import deque

from models.cell import Cell
from models.direction import Direction
from models.canvas import Canvas
from models.config_parser import ConfigParser
from models.renderer import Renderer


class MazeGenerator():
    """Generates, solves and renders mazes."""

    def __init__(self, config_file: str) -> None:
        """Initialize maze generator from config file.

        Args:
            config_file: Path to configuration file.
        """
        config = ConfigParser().parse_config(config_file)
        if not config:
            print("Failed to load configuration. Exiting.")
            sys.exit(1)
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]
        self.seed = config["SEED"]
        self.algorithm = config["ALGORITHM"]
        self.output_file = config["OUTPUT_FILE"]
        self.rng = random.Random(self.seed)

    def set_canvas(self) -> None:
        """Initialize maze canvas.

        Raises:
            ValueError: If entry/exit overlaps with '42' pattern.
        """
        self.canvas = Canvas(self.width, self.height, self.entry, self.exit)
        if self.width >= 9 and self.height >= 7:
            self.put_ft_cells()

            entry_cell = self.canvas.get_cell(self.entry[0], self.entry[1])
            if entry_cell in self.canvas.ft_cells:
                raise ValueError(
                    "Please change entry coordinates. "
                    "It is reserved for '42' pattern"
                )

            exit_cell = self.canvas.get_cell(self.exit[0], self.exit[1])
            if exit_cell in self.canvas.ft_cells:
                raise ValueError(
                    "Please change exit coordinates. "
                    "It is reserved for '42' pattern"
                )

    def set_renderer(self, color_index: int = 0) -> None:
        """Initialize maze renderer.

        Args:
            color_index: Starting color index for walls.
        """
        self.renderer = Renderer(
            self.canvas.width,
            self.canvas.height,
            self.canvas.entry,
            self.canvas.exit,
            [],
            "",
            color_index
        )
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                cell = self.canvas.get_cell(x, y)
                if cell:
                    self.renderer.cells.append(cell)

    def generate_maze(self) -> None:
        """Generate maze using selected algorithm."""
        try:
            if self.algorithm == "dfs":
                from algorithms.dfs import generate_maze
            elif self.algorithm == "hunt_and_kill":
                from algorithms.hunt_and_kill import generate_maze

            for _ in generate_maze(
                self.canvas, self.canvas.cells[0], self.rng
            ):
                self.renderer.render_maze()
                time.sleep(0.01)

            if not self.perfect:
                self.remove_dend_walls()

            while self.has_forbidden_opened_block():
                self.set_canvas()
                generate_maze(self.canvas, self.canvas.cells[0], self.rng)
                if not self.perfect:
                    self.remove_dend_walls()

        except AttributeError as e:
            print("Got error:", e)

    def regenerate_maze(self) -> None:
        """Regenerate maze with the same settings."""
        self.renderer.show_path = False
        self.rng = random.Random(self.seed)
        self.set_canvas()
        self.set_renderer(self.renderer.color_index)
        self.generate_maze()

    def remove_dend_walls(self) -> None:
        """Remove some dead-end walls for imperfect mazes."""
        if not len(self.canvas.dead_ends):
            return
        for _ in range(len(self.canvas.dead_ends) // 5 + 1):
            cell, neighbour = self.rng.choice(self.canvas.dead_ends)
            self.canvas.remove_wall(cell, neighbour)

    def put_ft_cells(self) -> None:
        """Place '42' pattern cells in the center."""
        x_mid = self.canvas.width // 2
        y_mid = self.canvas.height // 2
        cells_to_close = [
            self.canvas.get_cell(x_mid - 3, y_mid - 2),
            self.canvas.get_cell(x_mid - 3, y_mid - 1),
            self.canvas.get_cell(x_mid - 3, y_mid),
            self.canvas.get_cell(x_mid - 2, y_mid),
            self.canvas.get_cell(x_mid - 1, y_mid),
            self.canvas.get_cell(x_mid - 1, y_mid + 1),
            self.canvas.get_cell(x_mid - 1, y_mid + 2),

            self.canvas.get_cell(x_mid + 1, y_mid - 2),
            self.canvas.get_cell(x_mid + 2, y_mid - 2),
            self.canvas.get_cell(x_mid + 3, y_mid - 2),
            self.canvas.get_cell(x_mid + 3, y_mid - 1),
            self.canvas.get_cell(x_mid + 3, y_mid),
            self.canvas.get_cell(x_mid + 2, y_mid),
            self.canvas.get_cell(x_mid + 1, y_mid),
            self.canvas.get_cell(x_mid + 1, y_mid + 1),
            self.canvas.get_cell(x_mid + 1, y_mid + 2),
            self.canvas.get_cell(x_mid + 2, y_mid + 2),
            self.canvas.get_cell(x_mid + 3, y_mid + 2)
        ]
        for cell in [cell for cell in cells_to_close if cell]:
            cell.is_visited = True
            self.canvas.ft_cells.append(cell)

    def solve_maze(self) -> None:
        """Solve maze using BFS and store the solution."""
        for cell in self.canvas.cells:
            cell.is_visited = False

        entry = self.canvas.entry
        entry_cell = self.canvas.get_cell(entry[0], entry[1])
        if not entry_cell:
            return

        queue = deque([(entry_cell, [entry_cell])])

        while queue:
            cell, path = queue.popleft()

            if not cell or cell.is_visited:
                continue

            cell.is_visited = True

            if cell.coordinate == self.canvas.exit:
                self.renderer.solution = self.convert_path_to_str(path)
                return

            for neighbour in self.canvas.get_accessible_neighbours(cell):
                if not neighbour.is_visited:
                    queue.append((neighbour, path + [neighbour]))

    def has_forbidden_opened_block(self) -> bool:
        """Check for forbidden 3x3 open areas.

        Returns:
            True if a forbidden open block exists.
        """
        opened_cells = {
            cell for cell in self.canvas.cells
            if cell.direction.value == Direction.OPENED.value
        }

        for opened_cell in opened_cells:
            x, y = opened_cell.coordinate
            north = self.canvas.get_cell(x, y - 1)
            south = self.canvas.get_cell(x, y + 1)
            west = self.canvas.get_cell(x - 1, y)
            east = self.canvas.get_cell(x + 1, y)

            if not north or not south or not west or not east:
                continue

            north_open = (
                north.direction.can_see(Direction.S)
                and north.direction.can_see(Direction.W)
                and north.direction.can_see(Direction.E)
            )

            south_open = (
                south.direction.can_see(Direction.N)
                and south.direction.can_see(Direction.W)
                and south.direction.can_see(Direction.E)
            )

            west_open = (
                west.direction.can_see(Direction.S)
                and west.direction.can_see(Direction.E)
                and west.direction.can_see(Direction.N)
            )

            east_open = (
                east.direction.can_see(Direction.S)
                and east.direction.can_see(Direction.W)
                and east.direction.can_see(Direction.N)
            )

            if not all([north_open, south_open, west_open, east_open]):
                continue

            return True

        return False

    def fill_output(self) -> None:
        """Write maze data to the output file."""
        with open(self.output_file, "w") as file:
            output = ""

            for y in range(self.canvas.height):
                for x in range(self.canvas.width):
                    cell = self.canvas.get_cell(x, y)
                    if cell:
                        output += f"{cell.direction.value:X}"
                output += "\n"

            entry_txt = ", ".join(map(str, self.canvas.entry))
            exit_txt = ", ".join(map(str, self.canvas.exit))

            output += (
                f"\n{entry_txt}\n"
                f"{exit_txt}\n"
                f"{self.renderer.solution}\n"
            )

            file.write(output)

    @staticmethod
    def convert_path_to_str(path: list[Cell]) -> str:
        """Convert path of cells to direction string.

        Args:
            path: List of cells in the path.

        Returns:
            String of directions (N, E, S, W).
        """
        directions: list[str] = []
        dir_map = {
            (0, -1): "N",
            (0,  1): "S",
            (-1, 0): "W",
            (1,  0): "E",
        }

        for cur_cell, nxt_cell in zip(path, path[1:]):
            dx = nxt_cell.coordinate[0] - cur_cell.coordinate[0]
            dy = nxt_cell.coordinate[1] - cur_cell.coordinate[1]
            directions.append(dir_map.get((dx, dy), ""))

        return "".join(directions)
