from models.Canvas import Canvas
from models.Cell import Cell
import random

def generate_maze(canvas: Canvas, start_cell: Cell) -> None:

    if not canvas or not start_cell:
        return
    
    stack = [start_cell]
    start_cell.is_visited = True

    while stack:
        cell = stack[-1]

        neighbours = canvas.get_neighbours(cell)
        unvisited = [neighbour for neighbour in neighbours if not neighbour.is_visited]
        if unvisited:
            neighbour = random.choice(unvisited)
            canvas.remove_wall(cell, neighbour)
            neighbour.is_visited = True
            stack.append(neighbour)
        else:
            inaccessible_neighbours = list(set(neighbours) - set(canvas.get_accessible_neighbours(cell)))
            inaccessible_neighbours = [neighbour for neighbour in inaccessible_neighbours if neighbour not in canvas.ft_cells]
            if inaccessible_neighbours:
                neighbour_behind_wall = random.choice(inaccessible_neighbours)
                canvas.dead_ends.add((cell, neighbour_behind_wall))
            stack.pop()
