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

    def draw_entity(self, position, tile_type):
        """
         Draws the entity with tile type at the given position using a coloured rectangle with
         superimposed text identifying the entity
        Args:
            position: (row, col)
            tile_type: entity type, find the color in ENTITY_COLOURS
        """
        self.create_rectangle(self.get_bbox(position), fill=ENTITY_COLOURS[tile_type])
        self.annotate_position(position, tile_type, fill=self._entity_fg[tile_type])

class InventoryView(AbstractGrid):
    """
    InventoryView is a view class which inherits from AbstractGrid and displays the items the player
    has in their inventory.
    """
    def __init__(self, master, rows, **kwargs):
        """

        Args:
            master:
            rows:  the number of rows in the game map
            **kwargs: any additional named arguments supported by tk.Canvas
        """
        height = rows * CELL_SIZE
        self._status_color = {
            True: DARK_PURPLE,
            False: LIGHT_PURPLE
        }
        self._fg_color = {
            True: WHITE,
            False: DARK_PURPLE
        }
        super().__init__(master=master, rows=rows, cols=2, width=INVENTORY_WIDTH, height=height, **kwargs)

    def draw(self, inventory):
        """
         Draws the inventory label and current items with their remaining lifetimes
        Args:
            inventory: the player's inventory
        """
        self.delete("all")
        self.draw_label()
        for index, item in enumerate(inventory.get_items()):
            self.draw_pickup(index+1, item, item.is_active())
    
    def draw_label(self):
        """
        Draw Inventory label and its size
        """
        x_min = 0
        y_min = 0
        x_max = self._cell_width * self._cols
        y_max = self._cell_height
        position = (x_min, y_min, x_max, y_max)
        self.create_rectangle(position, fill=LIGHT_PURPLE, outline=LIGHT_PURPLE)
        position_center = ((x_min + x_max) / 2, (y_min + y_max) / 2)
        self.create_text(position_center, text="Inventory", fill=DARK_PURPLE, font="None 14")

    def draw_pickup(self, row, item, is_active):
        """
        draw the row in inventory view according to the given index
        Args:
            row: row
            item: Pickup
        """
        pickup_text = {
            GARLIC: "Garlic",
            CROSSBOW: "Crossbow"
        }
        col = 0
        position = (col, row)
        self.create_rectangle(self.get_bbox(position), fill=self._status_color[is_active], outline=self._status_color[is_active])
        self.annotate_position(position, pickup_text[item.display()], fill=self._fg_color[is_active])

        col = 1
        position = (col, row)
        self.create_rectangle(self.get_bbox(position), fill=self._status_color[is_active], outline=self._status_color[is_active])
        self.annotate_position(position, str(item.get_lifetime()), fill=self._fg_color[is_active])

    def toggle_item_activation(self, pixel, inventory):
        """
        Activates or deactivates the item (if one exists) in the row containing the pixel.
        Args:
            pixel: location (x, y)
            inventory: the player's inventory

        Returns:
            whether the item can be activated or deactivated
        """
        row, col = self.pixel_to_position(pixel)
        if row > len(inventory.get_items()):
            return False

        if inventory.any_active():
            for index, pickup in enumerate(inventory.get_items()):
                if pickup.is_active() and index + 1 != row:
                    return True
                if pickup.is_active() and index + 1 == row:
                    inventory.get_items()[index].toggle_active()
                    self.draw_pickup(row, pickup, pickup.is_active())
        else:
            for index, pickup in enumerate(inventory.get_items()):
                if index + 1 == row:
                    inventory.get_items()[index].toggle_active()
                    self.draw_pickup(row, pickup, pickup.is_active())
        return False

class BasicGraphicalInterface:
    """
    The BasicGraphicalInterface should manage the overall view (i.e. constructing the three
    major widgets) and event handling.
    """
    def __init__(self, root, size):
        """

        Args:
            root: the root window
            size: the number of rows (= number of columns) in the game map
        """
        self._master = root
        self._size = size

        self._master.title("EndOfDayZ")

        self._game = None
        self._step_schedule = None

        self._title = tk.Label(self._master, text="End Of DayZ", bg=DARK_PURPLE,
                               font="None 16 bold", fg=WHITE)
        self._title.pack(side=tk.TOP, fill=tk.BOTH)

        self._grid_width = self._grid_height = size * CELL_SIZE
        self._width = self._grid_width + INVENTORY_WIDTH
        self._main_container = tk.Canvas(self._master, width=self._width, height=self._grid_height)
        self._main_container.pack(side=tk.TOP, fill=tk.BOTH)

        self._grid = BasicMap(self._main_container, size=size, bg=LIGHT_BROWN)
        self._grid.pack(side=tk.LEFT)

        self._inventory = InventoryView(self._main_container, rows=size, bg=LIGHT_PURPLE)
        self._inventory.pack(side=tk.LEFT)

    def draw(self, game):
        """
        Clears and redraws the view based on the current game state.
        Args:
            game:

        Returns:

        """
        self._grid.delete("all")

        for entity_position, tile_type in game.get_grid().get_mapping().items():
            x = entity_position.get_x()
            y = entity_position.get_y()
            self._grid.draw_entity((x, y), tile_type.display())

        inventory = game.get_player().get_inventory()
        self._inventory.draw(inventory=inventory)

        self._grid.unbind_all("<Any-KeyPress>")
        self._grid.bind_all("<Any-KeyPress>", lambda event, func=self.key_press, is_fire=self.is_fire(): self.key_press(event, is_fire))

    def key_press(self, event, is_fire):
        """
        Tap on the keyboard input
        Args:
            event:
        """
        direction = event.char.upper()
        if is_fire:
            self._fire(direction)
        else:
            self._move(direction)

    def _move(self, direction):
        """
        Handles moving the player and redrawing the game.
        Args:
            direction: direction

        Returns:

        """
        if direction in DIRECTIONS:
            offset = self._game.direction_to_offset(direction)
            if offset is not None:
                self._game.move_player(offset)
            self.draw(self._game)

            self.quit_game()

    def is_fire(self):
        inventory = self._game.get_player().get_inventory()
        return inventory.has_active(CROSSBOW)

    def _fire(self, direction):
        """
        Handles the fire of crossbow and redrawing the game.
        Args:
            direction: direction

        Returns:

        """
        if direction in DIRECTIONS:
            # function handle_action in a2.solution.py
            start = self._game.get_grid().find_player()
            offset = self._game.direction_to_offset(direction)
            if start is None or offset is None:
                return  # Should never happen.

            # Find the first entity in the direction player fired.
            first = a2.first_in_direction(
                self._game.get_grid(), start, offset
            )

            # If the entity is a zombie, kill it.
            if first is not None and first[1].display() in ZOMBIES:
                position, entity = first
                self._game.get_grid().remove_entity(position)
                self.draw(self._game)
            else:
                print(NO_ZOMBIE_MESSAGE)

    def quit_game(self):
        """
        determine whether to quit the game
        Returns:

        """
        quit_game = False
        message = ""
        if self._game.has_won():
            message = WIN_MESSAGE
            quit_game = True

        if self._game.has_lost():
            message = LOSE_MESSAGE
            quit_game = True

        if quit_game:
            self._master.after_cancel(self._step_schedule)
            messagebox.showinfo(title=message, message=message)
            if messagebox.askyesno("Quit?", "Are you sure you want to quit?"):
                self._master.destroy()
        return quit_game

    def _step(self, game):
        """
        The step method triggers the step method for the game and updates the view accordingly.

        The step method is called every second.

        Args:
            game:

        Returns:

        """
        self._master.update()
        game.step()
        self.draw(game)

        if not self.quit_game():
            self._step_schedule = self._master.after(STEP_FPS, self._step, game)

    def _inventory_click(self, event, inventory):
        """
        This method should be called when the user left clicks on inventory view.

        It must handle activating or deactivating the clicked item (if one exists) and
        update both the model and the view accordingly.

        Args:
            event: click event
            inventory: inventory

        Returns:

        """
        position = (event.x, event.y)
        if self._inventory.toggle_item_activation(position, inventory):
            messagebox.showinfo(title="Alert", message="Only one item may be active at any given time!")
            return

        self._inventory.bind("<Button-1>", lambda event, func=self._inventory_click, inventory=inventory: self._inventory_click(event, inventory))

        self._grid.unbind_all("<Any-KeyPress>")
        self._grid.bind_all("<Any-KeyPress>", lambda event, func=self.key_press, is_fire=self.is_fire(): self.key_press(event, is_fire))
