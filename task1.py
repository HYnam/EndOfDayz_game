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
        x, y = position
        x_min = x * self._cell_width
        y_min = y * self._cell_height
        x_max = x * self._cell_width + self._cell_width
        y_max = y * self._cell_height + self._cell_height
        return x_min, y_min, x_max, y_max

    def pixel_to_position(self, pixel):
        """
        Converts the (x, y) pixel position (in graphics units) to a (row, column) position.
        """
        x, y = pixel
        position = (y // self._cell_height, x // self._cell_width)
        return position

    def get_position_center(self, position):
        """
        Gets the graphics coordinates for the center of the cell at the given (row, column) position.
        
        Args:
            position: (row, column)

        Returns:
            (x, y)
        """
        x_min, y_min, x_max, y_max = self.get_bbox(position)
        position_center = ((x_min + x_max) / 2, (y_min + y_max) / 2)
        return position_center

    def annotate_position(self, position, text):
        """
        Annotates the center of the cell at the given (row, column) position with the provided text.
        
        Args:
            position: (row, column)
            text: string for annotation
            **kwargs
        """
        self.create_text(self.get_position_center(position), text=text, **kwargs)

class BasicMap(AbstractGrid):
    """
    BasicMap is a view class which inherits from AbstractGrid.

    Entities are drawn on the map using coloured rectangles at different (row, column) positions.
    """
    def __init__(self, master, size, **kwargs):
        """

        Args:
            master:
            size:  the number of rows (= number of columns) in the grid
            **kwargs:
        """
        width = size * CELL_SIZE
        height = size * CELL_SIZE
        self._size = size
        self._entity_fg = {
            PLAYER: WHITE,
            HOSPITAL: WHITE,
            ZOMBIE: BLACK,
            GARLIC: BLACK,
            TRACKING_ZOMBIE: BLACK,
            CROSSBOW: BLACK
        }
        super().__init__(master=master, rows=size, cols=size, width=width, height=height, **kwargs)
