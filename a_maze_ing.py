"""Main program for maze generator."""

import sys
from models.maze_generator import MazeGenerator


if __name__ == "__main__":
    """Run main program."""
    maze_generator = MazeGenerator("config.txt")

    try:
        maze_generator.set_canvas()
    except ValueError as e:
        print(e)
        sys.exit(1)

    maze_generator.set_renderer()
    maze_generator.generate_maze()
    maze_generator.solve_maze()
    maze_generator.fill_output()

    renderer = maze_generator.renderer

    try:
        while True:
            renderer.render_maze()
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
        exit(1)
