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

    def get_bbox(self, position):
        """
        Returns the bounding box for the (row, column) position
        """
        position = (self.rows, self.cols)
        return position

    def pixel_to_position(self, pixel):
        """
        Converts the (x, y) pixel position (in graphics units) to a (row, column) position.
        """
        pass

    def get_position_center(self, position):
        """
        Gets the graphics coordinates for the center of the cell at the given (row, column) position.
        """
        pass

    def annotate_position(self, position, text):
        """
        Annotates the center of the cell at the given (row, column) position with the provided text.
        """
        pass