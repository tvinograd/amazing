# Main program file 

# Errors to handle:
# - invalid configuration
# - file not found
# - bad syntax
# - impossible maze parameters, etc

# For config.txt:
# - Lines starting with # are comments and must be ignored

# For output_maze.txt:
# - maze using one hexadecimal digit per cell, where each digit encodes which walls are closed:
# | Bit     | Direction |
# |---------------------|
# | 0 (LSB) | North     |
# | 1       | East      |
# | 2       | South     |
# | 3       | West      |
# Closed wall sets bit to 1, open - 0: (MIGHT BE WRONG)
# Binary  Hex  W  S  E  N
# -----------------------
# 0000    0    O  O  O  O
# 0001    1    O  O  O  C
# 0010    2    O  O  C  O
# 0011    3    O  O  C  C
# 0100    4    O  C  O  O
# 0101    5    O  C  O  C
# 0110    6    O  C  C  O
# 0111    7    O  C  C  C
# 1000    8    C  O  O  O
# 1001    9    C  O  O  C
# 1010    A    C  O  C  O
# 1011    B    C  O  C  C
# 1100    C    C  C  O  O
# 1101    D    C  C  O  C
# 1110    E    C  C  C  O
# 1111    F    C  C  C  C
# - entry coordinates (e.g., 1,1) \n
# - exit coordinates \n
# - shortest valid path (e.g. SWENSWENS)

# Maze requirements:
# - each cell: 0 - 4 walls
# - entry and exit are different, inside the maze bounds
# - no isolated cells
# - each neighbouring cell must have the same wall if an
# - no large open areas: corridors not wider than 2 cells
# - "42" closed cells in the middle (error if maze size is too small)
# - PERFECT == only one path

# User options after visualisation:
# 1. Re-generate a new maze
# 2. Show/Hide path from empty entry to exit
# 3. Rotate maze colors
# 4. Quit
# Choise? (1-4): 


import random
from models.MazeGenerator import MazeGenerator

# def print_canvas(canvas: Canvas) -> None:
#     for y in range(canvas.height):
#         for x in range(canvas.width):
#             cell = canvas.get_cell(x, y)
#             print(f"{cell.direction.get_unicode()}", end=" ")
#         print()
#     print()
#     print(*canvas.entry, sep=", ")
#     print(*canvas.exit, sep=", ")


# def print_canvas_visits(canvas: Canvas) -> None:
#     print()
#     for y in range(canvas.height):
#         for x in range(canvas.width):
#             cell = canvas.get_cell(x, y)
#             print("0" if cell.is_visited else "-", end=" ")
#         print()

from models.Canvas import Canvas
def print_canvas_values(canvas: Canvas) -> None:
    for y in range(canvas.height):
        for x in range(canvas.width):
            cell = canvas.get_cell(x, y)
            print(f"{cell.direction.value:x}".upper(), end="")
        print()

# def print_dead_ends(canvas: Canvas) -> None:
#     for cell1, cell2 in canvas.dead_ends:
#         print(cell1.coordinate, cell2.coordinate, end=" ")
#         print()


if __name__ == "__main__":
    width = 5
    height = 5
    entry = (0, 0)
    exit = (4, 4)

    # random.seed(42)

    maze_generator = MazeGenerator()
    maze_generator.set_canvas(width, height, entry, exit)
    # maze_generator.set_renderer()
    maze_generator.generate_maze() # perfect
    # maze_generator.generate_maze(False) # imperfect
    maze_generator.solve_maze()

    try:
        while True:
            # maze_generator.renderer.render_maze()
            print_canvas_values(maze_generator.canvas)
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ")

            if choice == "1":
                maze_generator.regenerate_maze() # perfect
                # maze_generator.regenerate_maze(False) # imperfect
                maze_generator.solve_maze()
            # elif choice == "2":
            #     maze_generator.renderer.show_path = not maze_generator.renderer.show_path
            # elif choice == "3":
            #     maze_generator.renderer.color_index = (maze_generator.renderer.color_index + 1) % len(maze_generator.renderer.wall_colors)
            elif choice == "4":
                print("Bye!")
                break
    except KeyboardInterrupt:
        print("\nBye!")
