"""Hunt and kill maze generation algorithm."""

import random
from typing import Generator

from models.canvas import Canvas
from models.cell import Cell


def generate_maze(
        canvas: Canvas,
        start_cell: Cell,
        rng: random.Random
) -> Generator[str, None, None]:
    """Generate a maze using hunt and kill algorithm.

    Args:
        canvas: The maze canvas to generate on.
        start_cell: Starting cell for generation.
        rng: Random number generator for reproducibility.

    Yields:
        Empty string for each step (for progress tracking).
    """
    cell = start_cell

    if not canvas or not cell:
        return

    while True:
        cell.is_visited = True
        neighbours = canvas.get_neighbours(cell)
        unvisited = [n for n in neighbours if not n.is_visited]

        if unvisited:
            neighbour = rng.choice(unvisited)
            canvas.remove_wall(cell, neighbour)
            cell = neighbour
        else:
            accessible = set(canvas.get_accessible_neighbours(cell))
            inaccessible = [
                n for n in neighbours
                if n not in accessible and n not in canvas.ft_cells
            ]
            if inaccessible:
                neighbour_behind_wall = rng.choice(inaccessible)
                canvas.dead_ends.append((cell, neighbour_behind_wall))

            found = False
            for y in range(canvas.height):
                for x in range(canvas.width):
                    hunt_cell = canvas.get_cell(x, y)
                    if hunt_cell and not hunt_cell.is_visited:
                        neighbours = canvas.get_neighbours(hunt_cell)
                        visited = [
                            n for n in neighbours
                            if n.is_visited and n not in canvas.ft_cells
                        ]
                        if visited:
                            neighbour = rng.choice(visited)
                            canvas.remove_wall(hunt_cell, neighbour)
                            cell = hunt_cell
                            found = True
                            break
                if found:
                    break

            if not found:
                break

        yield ""
