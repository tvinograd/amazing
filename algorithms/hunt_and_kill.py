from models.canvas import Canvas
from models.cell import Cell
from typing import Generator
import random

def generate_maze(canvas: Canvas, cell: Cell, rng: random.Random) -> Generator[str, None, None]:

    if not canvas or not cell:
        return

    while True:
        cell.is_visited = True

        neighbours = canvas.get_neighbours(cell)
        unvisited = [neighbour for neighbour in neighbours if not neighbour.is_visited]
        if unvisited:
            neighbour = rng.choice(unvisited)
            canvas.remove_wall(cell, neighbour)
            cell = neighbour
        else:
            accessible_neighbours = set(canvas.get_accessible_neighbours(cell))
            inaccessible_neighbours = [neighbour for neighbour in neighbours if neighbour not in accessible_neighbours and neighbour not in canvas.ft_cells]
            if inaccessible_neighbours:
                neighbour_behind_wall = rng.choice(inaccessible_neighbours)
                canvas.dead_ends.append((cell, neighbour_behind_wall))

            found = False
            for y in range(canvas.height):
                for x in range(canvas.width):
                    cell = canvas.get_cell(x, y)
                    if not cell.is_visited:
                        neighbours = canvas.get_neighbours(cell)
                        visited = [neighbour for neighbour in neighbours if neighbour.is_visited and neighbour not in canvas.ft_cells]
                        if visited:
                            neighbour = rng.choice(visited)
                            canvas.remove_wall(cell, neighbour)
                            found = True
                            break
                if found:
                    break
            if not found:
                break
        yield ""
