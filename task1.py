import tkinter as tk
import tkinter.messagebox as messagebox

import a2_solution as a2
from constants import *

class AbstractGrid(tk.Canvas):
    """
    provides base functionality for other view classes. An AbstractGrid can be thought of as a grid.
    """
    def __init__(self, master, rows, cols, width, height, **kwargs):
        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        self._cell_width = self._width // self._cols
        self._cell_height = self._height // self._rows
        super().__init__(master, **kwargs)
        self.config(width=width, height=height)

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