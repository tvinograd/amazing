"""Maze generator package."""

from mazegen.maze_generator import MazeGenerator
from mazegen.canvas import Canvas
from mazegen.cell import Cell
from mazegen.direction import Direction
from mazegen.config_parser import ConfigParser
from mazegen.renderer import Renderer

__all__ = [
    "MazeGenerator",
    "Canvas",
    "Cell",
    "Direction",
    "ConfigParser",
    "Renderer",
]

__version__ = "1.0.0"
