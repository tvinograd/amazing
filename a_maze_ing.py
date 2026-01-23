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
# Binary  Hex  N  E  S  W
# -----------------------
# 0000    0    O  O  O  O
# 0001    1    C  O  O  O
# 0010    2    O  C  O  O
# 0011    3    C  C  O  O
# 0100    4    O  O  C  O
# 0101    5    C  O  C  O
# 0110    6    O  C  C  O
# 0111    7    C  C  C  O
# 1000    8    O  O  O  C
# 1001    9    C  O  O  C
# 1010    A    O  C  O  C
# 1011    B    C  C  O  C
# 1100    C    O  O  C  C
# 1101    D    C  O  C  C
# 1110    E    O  C  C  C
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
