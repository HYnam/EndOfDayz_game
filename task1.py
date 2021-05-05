import tkinter as tk
import typing
import math
import tkinter.messagebox
import PIL

from a2_solution import advanced_game
from constants import TASK, MAP_FILE

class AbstractGrid(tk.Canvas):
    """
    provides base functionality for other view classes. An AbstractGrid can be thought of as a grid.
    """
    def __init__(self, master, rows, cols, width, height, **kwargs):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height