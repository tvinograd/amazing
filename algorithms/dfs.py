from models.canvas import Canvas
from models.cell import Cell
import random

def generate_maze(canvas: Canvas, start_cell: Cell, rng: random.Random) -> None:

    if not canvas or not start_cell:
        return
    
    stack = [start_cell]
    start_cell.is_visited = True

    while stack:
        cell = stack[-1]

        neighbours = canvas.get_neighbours(cell)
        unvisited = [neighbour for neighbour in neighbours if not neighbour.is_visited]
        if unvisited:
            neighbour = rng.choice(unvisited)
            canvas.remove_wall(cell, neighbour)
            neighbour.is_visited = True
            stack.append(neighbour)
        else:
            accessible_neighbours = set(canvas.get_accessible_neighbours(cell))
            inaccessible_neighbours = [neighbour for neighbour in neighbours if neighbour not in accessible_neighbours and neighbour not in canvas.ft_cells]
            if inaccessible_neighbours:
                neighbour_behind_wall = rng.choice(inaccessible_neighbours)
                canvas.dead_ends.add((cell, neighbour_behind_wall))
            stack.pop()
