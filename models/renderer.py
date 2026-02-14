import time
from enum import Enum


class Presets(Enum):
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
    walls = [
        (1, -1,  0, -1, +1),  # North: wall above + corner above-right
        (2,  0, +1, +1, +1),  # East:  wall right + corner below-right
        (4, +1,  0, +1, -1),  # South: wall below + corner below-left
        (8,  0, -1, -1, -1),  # West:  wall left  + corner above-left
    ]

    sol_mov = {
        "N": (-1, 0),  # North: row - 1
        "E": (0, +1),  # East:  col + 1
        "S": (+1, 0),  # South: row + 1
        "W": (0, -1),  # West:  col - 1
    }

    wall_colors = [Presets.WHITE, Presets.YELLOW, Presets.GREY, Presets.CYAN]

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], cells: list[int], solution: str):
        self.width = width
        self.height = height
        self.cells = cells
        self.solution = solution

        self.color_index = 0
        self.show_path = False
        self.path_animated = False
        self.grid_width = width * 2 + 1
        self.grid_height = height * 2 + 1
        self.entry_y = entry[1] * 2 + 1
        self.entry_x = entry[0] * 2 + 1
        self.exit_y = exit[1] * 2 + 1
        self.exit_x = exit[0] * 2 + 1

    def render_maze(self) -> None:
        try:
            print("\033c", end="")
            colored_wall = (f"{self.wall_colors[self.color_index].value}"
                            f"{Presets.WALL.value}{Presets.RESET.value}")

            # Grid
            grid: list[list[str]] = [
                [Presets.PATH.value for _ in range(self.grid_width)]
                for _ in range(self.grid_height)
            ]

            for row in range(self.height):
                for col in range(self.width):
                    cell = self.cells[row * self.width + col]
                    y = row * 2 + 1
                    x = col * 2 + 1

                    for bit, wall_y, wall_x, corner_y, corner_x in self.walls:
                        if cell & bit:
                            grid[y + wall_y][x + wall_x] = colored_wall
                            grid[y + corner_y][x + corner_x] = colored_wall

                    # Fully closed
                    if cell == 15:
                        grid[y][x] = (f"{Presets.GREEN.value}"
                                      f"{Presets.WALL.value}"
                                      f"{Presets.RESET.value}")

            # Entry / exit
            grid[self.entry_y][self.entry_x] = (f"{Presets.MAGENTA.value}"
                                                f"{Presets.WALL.value}"
                                                f"{Presets.RESET.value}")
            grid[self.exit_y][self.exit_x] = (f"{Presets.RED.value}"
                                              f"{Presets.WALL.value}"
                                              f"{Presets.RESET.value}")

            # Solution path
            if self.show_path:
                sol_y = self.entry_y
                sol_x = self.entry_x
                for step in self.solution:
                    step_y, step_x = self.sol_mov[step]

                    # Wall unit
                    sol_y += step_y
                    sol_x += step_x
                    grid[sol_y][sol_x] = (f"{Presets.BLUE.value}"
                                          f"{Presets.WALL.value}"
                                          f"{Presets.RESET.value}")

                    # Cell unit
                    sol_y += step_y
                    sol_x += step_x
                    if not (sol_y == self.exit_y and sol_x == self.exit_x):
                        grid[sol_y][sol_x] = (f"{Presets.BLUE.value}"
                                              f"{Presets.WALL.value}"
                                              f"{Presets.RESET.value}")

                    # Draw path (first time)
                    if not self.path_animated:
                        print("\033c", end="")
                        for row_printed in grid:
                            print("".join(row_printed))
                        time.sleep(0.05)
                    
                if not self.path_animated:
                    self.path_animated = True
                    return

            # Draw maze
            for row_printed in grid:
                print("".join(row_printed))

        except KeyboardInterrupt:
            print("\nBye!")
            exit(1)
        except Exception as e:
            print(f"Error while rendering: {e}")
