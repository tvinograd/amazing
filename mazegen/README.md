# MazeGen Documentation

Python maze generator and solver package.

## Installation
```bash
[uv] pip install mazegen-1.0.0-py3-none-any.whl
```

## Basic Usage

### Instantiate the Generator

The `MazeGenerator` class requires a configuration file path:
```python
from mazegen import MazeGenerator

generator = MazeGenerator(<filename>)
```

### Configuration File Format

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

### Generate and Solve
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