*This project has been created as part of the 42 curriculum by tvinogra, iiunusov.*

# 📖 Description
**A-Maze-ing** is a configurable maze generator written in Python.  
It reads a configuration file, generates a maze according to specified parameters, ensures structural validity constraints, optionally enforces perfect-maze properties, writes the result to a file using a hexadecimal wall encoding format, and provides an interactive visual representation.

The project emphasizes:

- Deterministic random generation (via seed)
- Strict structural validity rules
- Perfect maze enforcement (optional)
- Modular and reusable architecture
- Clean error handling
- Packaging of a reusable maze generation module

---

## 🧠 Project Overview

The program:

1. Parses a configuration file (`KEY=VALUE` format).
2. Validates parameters.
3. Generates a maze satisfying strict structural constraints.
4. Embeds a visible “42” pattern using fully closed cells.
5. Optionally ensures the maze is perfect (exactly one path between entry and exit).
6. Writes the maze to an output file using hexadecimal encoding.
7. Provides a visual ASCII interface with user interaction.
8. Exposes a reusable module (`mazegen-*`) installable via pip.

---

## 🧩 Maze Requirements Compliance

The generated maze satisfies:

- Entry and exit inside bounds
- Entry ≠ Exit
- External border walls enforced
- Coherent neighbouring walls
- No isolated cells
- Full connectivity (except “42” pattern cells)
- No 3×3 fully open areas
- Corridors max width = 2 cells
- Optional perfect maze property
- Deterministic generation using seed

---


## 🧠 Maze Generation Algorithm

The project implements two maze generation algorithms:

- Iterative Depth-First Search (DFS)
- Hunt-and-Kill

Both algorithms ensure full connectivity of the maze while respecting structural constraints (no large open areas, coherent walls, external borders, etc.). The choice of algorithm can be configured via the configuration file.

### Why These Algorithms?

Both DFS and Hunt-and-Kill:

- Guarantee full connectivity
- Are simple to implement
- Allow deterministic generation via seed
- Respect structural constraints required by the subject
- Scale efficiently for large mazes
- Providing two algorithms allows experimentation with different maze styles while maintaining correctness and reproducibility.

If `PERFECT=True`, no additional walls are removed afterward.

If `PERFECT=False`, controlled additional openings may be added without violating structural constraints.

---

# Instructions

## ⚙️ Usage

### ▶️ Run the Program

```bash
make run
```
or
```bash
python3 a_maze_ing.py config.txt
```
- `a_maze_ing.py` — main program (mandatory name)
- `config.txt` — configuration file (mandatory argument)

The program handles:
- Missing file
- Invalid syntax
- Invalid parameters
- Impossible configurations
- Invalid entry/exit positions
- Maze too small for “42” pattern

It **never crashes unexpectedly** and always prints clear error messages.

---
## 🛠 Makefile Rules

The project includes a `Makefile` with:

| Rule | Description |
|-------|-------------|
| install | Install dependencies |
| run | Run the main program |
| debug | Run with pdb |
| clean | Remove caches (\_\_pycache__, .mypy_cache, .pyc) |
| lint | flake8 + mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs |
| lint-strict | flake8 + mypy --strict |

---

## MazeGen Documentation

Python maze generator and solver package.

### Installation
```bash
[uv] pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic Usage

#### Instantiate the Generator

The `MazeGenerator` class requires a configuration file path:
```python
from mazegen import MazeGenerator

generator = MazeGenerator(<filename>)
```

#### Configuration File Format

Create a configuration file (.txt) with these required keys:
```
WIDTH
HEIGHT
ENTRY
EXIT
OUTPUT_FILE
PERFECT
```

Optional keys:
```
SEED
ALGORITHM
```

#### Generate and Solve
```python
# Initialize the canvas (maze grid)
generator.set_canvas()

# Initialize the renderer (optional)
generator.set_renderer()

# Generate the maze
generator.generate_maze()

# Solve the maze (find shortest path)
generator.solve_maze()

# Write output to file
generator.fill_output()
```

## Custom Parameters

### Size

Set maze dimensions in the config file:
```
WIDTH=30
HEIGHT=20
```

### Entry and Exit

Coordinates are (x, y) starting from (0, 0) at top-left:
```
ENTRY=0,0
EXIT=29,19
```

### Seed

For reproducible mazes, set a seed:
```
SEED=42
```

Same seed produces identical maze every time.

### Algorithm

Two algorithms are available:
```
ALGORITHM=dfs
```

or
```
ALGORITHM=hunt_and_kill
```

Default is `dfs` (depth-first search).

### Perfect Maze
```
PERFECT=True
```

- `True`: Single solution path, no loops
- `False`: Multiple paths possible

## Accessing Generated Structure

### The Grid

Access individual cells through the canvas:
```python
# Get cell at coordinates (x, y)
cell = generator.canvas.get_cell(5, 10)

# Cell properties
print(cell.coordinate)  # (5, 10)
print(cell.direction)   # Direction enum (wall configuration)
print(cell.direction.value)  # Integer 0-15
```

### All Cells

Iterate through all cells:
```python
for cell in generator.canvas.cells:
    x, y = cell.coordinate
    walls = cell.direction.value
    print(f"Cell ({x},{y}): walls={walls}")
```

Or by coordinates:
```python
for y in range(generator.height):
    for x in range(generator.width):
        cell = generator.canvas.get_cell(x, y)
        print(f"{cell.direction.value:X}", end="")
    print()
```

## Accessing the Solution

### Solution String

After calling `solve_maze()`, the solution is stored as a direction string:
```python
generator.solve_maze()
path = generator.canvas.solution
print(path)  # "SSEENNEEESSSSWWW"
```
The shortest path between entry and exit is computed using **Breadth-First Search (BFS)**.

This guarantees:

- Shortest valid path
- Deterministic output
- Correct path encoding

The path is written using:
```
N E S W
```

## Output File

Call `fill_output()` to write the maze to a file:
```python
generator.fill_output()
```

Output format:
```
F9B3A5C7...    <- Hex grid (one row per line)
E4D2B8A1...
...

0, 0           <- Entry coordinates
19, 14         <- Exit coordinates
SSEENNEESS...  <- Solution path
```

## Complete Example
```python
from mazegen import MazeGenerator

# Create generator
generator = MazeGenerator("config.txt")

# Setup
generator.set_canvas()
# Create and set a renderer if necessary.
generator.set_renderer()

# Generate and solve
generator.generate_maze()
generator.solve_maze()

# Access maze data
print(f"Size: {generator.width}x{generator.height}")
print(f"Entry: {generator.entry}")
print(f"Exit: {generator.exit}")
print(f"Solution: {generator.canvas.solution}")
print(f"Solution length: {len(generator.canvas.solution)} steps")

# Print maze as hex
for y in range(generator.height):
    for x in range(generator.width):
        cell = generator.canvas.get_cell(x, y)
        print(f"{cell.direction.value:X}", end="")
    print()

# Save to file
generator.fill_output()
```

## Regenerating

To generate a new maze with the same settings:
```python
generator.regenerate_maze()
generator.solve_maze()
```

This resets the random number generator if a seed was provided, producing the same maze.

---

## 🎨 Visual Representation

The maze is rendered in the terminal using ASCII characters.

It displays:

- Walls
- Entry
- Exit
- Optional solution path

User interactions:

- Regenerate maze
- Show / hide shortest path
- Change wall colors
- Quit program

---

## 🔁 Code Reusability — mazegen Package

The maze generation logic is implemented in a standalone reusable module:

```
mazegen-<version>.whl
```

Located at repository root.

It can be built using standard Python packaging tools.

---

# 👥 Team & Project Management

## Roles

🧠 iiunusov — Architecture & Core Algorithms
- Implemented the reusable MazeGenerator module
- Developed the DFS and Hunt-and-Kill algorithms
- Implemented shortest path solver (BFS)
- Ensured seed-based deterministic generation
- Implemented output file encoding (hex format)
- Wrote Makefile and lint automation

🎨 tvinogra — Configuration, UI & Integration
- Implemented configuration file parsing and validation
- Handled packaging (mazegen-* module)
- Maintained mypy compliance and type safety
- Designed error handling and user-friendly messages
- Developed ASCII rendering system
- Implemented user interactions (regeneration, path toggle, color change)

---
## 🤝 Collaboration Model

Although responsibilities were divided, major architectural decisions were made together:

- Algorithm selection
- Structural constraint design
- Data model design (Cell / Canvas / Generator separation)
- Packaging strategy

All critical parts were reviewed jointly before final integration.

---

## Planning Evolution

Initial Plan:
- OOP approach
- Recursive DFS
- ASCII renderer

Evolution:
- Switched to iterative DFS
- Added strict structural validation
- Added deterministic seed control
- Implemented BFS solver
- Built reusable package
- Added interactive display
- Added animation while generating a maze and drawing a path

---

## What Worked Well

- Clear division of responsibilities
- Modular architecture
- Deterministic generation
- Packaging as reusable module

---

## What Could Be Improved

- Multiple generation algorithms

---

## Tools Used

- Python 3.10+
- Git
- flake8
- mypy
- virtualenv
- setuptools / build

All core design decisions were implemented and validated manually.

---

# 📚 Resources

- Introduction to Algorithms (CLRS) — [DFS & BFS](https://en.wikipedia.org/wiki/Introduction_to_Algorithms)
- Python official documentation — https://docs.python.org/3/
- Packaging Python Projects — [Python Packaging Authority](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- AI assistance for:
  - Debugging algorithm edge cases
  - Refactoring DFS
  - Documentation structuring

---

# 🚀 Advanced features

- Support multiple maze generation algorithms
- Animation during maze generation
- Animation while drawing a path
- Checking the terminal size before rendering
- Checking the terminal size during rendering
- Interrupt signal handling
