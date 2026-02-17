"""Terminal maze renderer using block characters."""

import select
import shutil
import signal
import sys
import time
from enum import Enum
from types import FrameType

from models.cell import Cell


class Presets(Enum):
    """ANSI color codes and block characters for rendering."""
    WALL = "██"
    PATH = "  "
    RESET = "\033[0m"
    GREY = "\033[90m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


class Renderer():
    """Renders maze to terminal with colors and animation."""
    walls = [
        (1, -1,  0, -1, +1),  # North: wall above + corner above-right
        (2,  0, +1, +1, +1),  # East:  wall right + corner below-right
        (4, +1,  0, +1, -1),  # South: wall below + corner below-left
        (8,  0, -1, -1, -1),  # West:  wall left  + corner above-left
    ]

    sol_mov = {
        "N": (0, -1),  # North: row - 1
        "E": (+1, 0),  # East:  col + 1
        "S": (0, +1),  # South: row + 1
        "W": (-1, 0),  # West:  col - 1
    }

    wall_colors = [Presets.WHITE, Presets.YELLOW, Presets.GREY, Presets.CYAN]

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            cells: list[Cell],
            solution: str,
            color_index: int = 0
    ) -> None:
        """Initialize the renderer.

        Args:
            width: Maze width in cells.
            height: Maze height in cells.
            entry: Entry coordinates (x, y).
            exit_: Exit coordinates (x, y).
            cells: List of maze cells.
            solution: Solution path as direction string.
            color_index: Starting wall color index.
        """
        self.width = width
        self.height = height
        self.cells = cells
        self.solution = solution

        self.color_index = color_index
        self.show_path = False
        self.path_animated = False
        self.grid_width = width * 2 + 1
        self.grid_height = height * 2 + 1
        self.entry_y = entry[1] * 2 + 1
        self.entry_x = entry[0] * 2 + 1
        self.exit_y = exit[1] * 2 + 1
        self.exit_x = exit[0] * 2 + 1

        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(
            self,
            _signum: int,
            _frame: FrameType | None
    ) -> None:
        """Handle termination signals."""
        print("\nBye!")
        sys.exit(0)

    def check_skip(self) -> bool:
        """Check if user pressed Enter to skip animation.

        Returns:
            True if Enter was pressed.
        """
        if select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()
            return True
        return False

    def check_terminal_size(self) -> bool:
        """Check if terminal is wide enough for the maze.

        Returns:
            True if rendering should proceed.
        """
        term_size = shutil.get_terminal_size()
        term_width = term_size.columns
        required_width = self.grid_width * 2

        if term_width < required_width:
            print(
                "\nYour terminal is not wide enough to display the maze "
                "correctly. We recommend resizing your window first."
            )
            size_choice = input("\nRender anyway? (y/n): ").lower().strip()
            return size_choice in ("y", "yes")

        return True

    def draw_grid(self, grid: list[list[str]]) -> None:
        """Clear screen and draw the grid.

        Args:
            grid: 2D list of characters to draw.
        """
        print("\033c", end="")
        for row_printed in grid:
            print("".join(row_printed))

    def render_maze(self) -> None:
        """Render maze to the terminal."""
        try:
            if not self.check_terminal_size():
                print("\nBye!")
                sys.exit(0)

            print("\033c", end="")
            colored_wall = (
                f"{self.wall_colors[self.color_index].value}"
                f"{Presets.WALL.value}{Presets.RESET.value}"
            )

            # Build grid
            grid: list[list[str]] = [
                [Presets.PATH.value for _ in range(self.grid_width)]
                for _ in range(self.grid_height)
            ]

            for row in range(self.height):
                for col in range(self.width):
                    cell = self.cells[row * self.width + col].direction.value
                    y = row * 2 + 1
                    x = col * 2 + 1

                    for bit, wall_y, wall_x, corner_y, corner_x in self.walls:
                        if cell & bit:
                            grid[y + wall_y][x + wall_x] = colored_wall
                            grid[y + corner_y][x + corner_x] = colored_wall

                    # Fully closed cell (42 pattern)
                    if cell == 15:
                        grid[y][x] = (
                            f"{Presets.GREEN.value}"
                            f"{Presets.WALL.value}"
                            f"{Presets.RESET.value}"
                        )

            # Entry and exit markers
            grid[self.entry_y][self.entry_x] = (
                f"{Presets.MAGENTA.value}"
                f"{Presets.WALL.value}"
                f"{Presets.RESET.value}"
            )
            grid[self.exit_y][self.exit_x] = (
                f"{Presets.RED.value}"
                f"{Presets.WALL.value}"
                f"{Presets.RESET.value}"
            )

            # Solution path
            if self.show_path:
                sol_y = self.entry_y
                sol_x = self.entry_x
                skip_animation = False

                for step in self.solution:
                    step_x, step_y = self.sol_mov[step]

                    # Wall unit
                    sol_y += step_y
                    sol_x += step_x
                    grid[sol_y][sol_x] = (
                        f"{Presets.BLUE.value}"
                        f"{Presets.WALL.value}"
                        f"{Presets.RESET.value}"
                    )

                    # Cell unit
                    sol_y += step_y
                    sol_x += step_x
                    if not (sol_y == self.exit_y and sol_x == self.exit_x):
                        grid[sol_y][sol_x] = (
                            f"{Presets.BLUE.value}"
                            f"{Presets.WALL.value}"
                            f"{Presets.RESET.value}"
                        )

                    # Animate only if the first time and not skipped
                    if not self.path_animated and not skip_animation:
                        self.draw_grid(grid)
                        time.sleep(0.05)

                        if self.check_skip():
                            skip_animation = True

                if not self.path_animated:
                    self.path_animated = True

                    if skip_animation:
                        self.draw_grid(grid)
                    return

            # Draw maze
            self.draw_grid(grid)

        except Exception as e:
            print(f"Error while rendering: {e}")
