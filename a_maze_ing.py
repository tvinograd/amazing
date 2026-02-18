"""Main program for maze generator."""

import sys
from models.maze_generator import MazeGenerator


if __name__ == "__main__":
    """Run main program."""

    if len(sys.argv) != 2:
        print("Wrong command format\n"
              "Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(0)

    maze_generator = MazeGenerator(sys.argv[1])

    try:
        maze_generator.set_canvas()
    except ValueError as e:
        print(e)
        sys.exit(0)

    maze_generator.set_renderer()
    maze_generator.generate_maze()
    maze_generator.solve_maze()
    maze_generator.fill_output()

    try:
        while True:
            renderer = maze_generator.renderer
            renderer.render_maze()
            if not maze_generator.is_size_suitable_ft():
                print("\n'42' pattern was omitted due to "
                      "the limited maze size.")
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ")

            if choice == "1":
                maze_generator.regenerate_maze()
                maze_generator.solve_maze()
                maze_generator.fill_output()
                renderer.path_animated = False
            elif choice == "2":
                renderer.show_path = not renderer.show_path
                if not renderer.show_path:
                    renderer.path_animated = False
            elif choice == "3":
                renderer.color_index = (
                    (renderer.color_index + 1) % len(renderer.wall_colors)
                )
            elif choice == "4":
                print("Bye!")
                break
    except Exception as e:
        print(f"Error: {e}")
