"""Depth-first search (dfs) maze generation algorithm."""

import random
from typing import Generator

from mazegen.canvas import Canvas
from mazegen.cell import Cell


def generate_maze(
        canvas: Canvas,
        start_cell: Cell,
        rng: random.Random
) -> Generator[str, None, None]:
    """Generate a maze using dfs algorithm.

    Args:
        canvas: The maze canvas to generate on.
        start_cell: Starting cell for generation.
        rng: Random number generator for reproducibility.

    Yields:
        Empty string for each step (for progress tracking).
    """
    if not canvas or not start_cell:
        return

    stack = [start_cell]
    start_cell.is_visited = True

    while stack:
        cell = stack[-1]
        neighbours = canvas.get_neighbours(cell)
        unvisited = [n for n in neighbours if not n.is_visited]

        if unvisited:
            neighbour = rng.choice(unvisited)
            canvas.remove_wall(cell, neighbour)
            neighbour.is_visited = True
            stack.append(neighbour)
        else:
            accessible = set(canvas.get_accessible_neighbours(cell))
            inaccessible = [
                n for n in neighbours
                if n not in accessible and n not in canvas.ft_cells
            ]
            if inaccessible:
                neighbour_behind_wall = rng.choice(inaccessible)
                canvas.dead_ends.append((cell, neighbour_behind_wall))
            stack.pop()

        yield ""
