import a2_solution as a2
from constants import *
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import tkinter.simpledialog as simpledialog
from typing import Tuple
from PIL import Image, ImageTk


class AbstractGrid(tk.Canvas):
    """
    AbstractGrid is an abstract view class which inherits from tk.Canvas and provides base
    functionality for other view classes.

    An AbstractGrid can be thought of as a grid with a set number of rows and columns,
    which supports creation of text at specific positions based on row and column.

    The number of rows may differ from the number of columns,
    and the cells may be non-square
    """
    # Same as task 1
    def __init__(self, master, rows, cols, width, height, **kwargs):
        """
        Args:
            master:
            rows: number of rows
            cols: number of cols
            width: the width of the grid in pixels
            height: the height of the grid in pixels
            **kwargs:
        """
        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height
        self._cell_width = self._width // self._cols
        self._cell_height = self._height // self._rows
        super().__init__(master, **kwargs)
        self.config(width=width, height=height)

    # Same as task 1
    def get_bbox(self, position):
        """
        Returns the bounding box for the position
        Args:
            position: (x, y)

        Returns:
            Returns the bounding box for the (x, y) position, in the form (x min, y min, x max, y max).

        """
        x, y = position
        x_min = x * self._cell_width
        y_min = y * self._cell_height
        x_max = x * self._cell_width + self._cell_width
        y_max = y * self._cell_height + self._cell_height
        return x_min, y_min, x_max, y_max

    # Same as task 1
    def pixel_to_position(self, pixel):
        """
         Converts the (x, y) pixel position (in graphics units) to a (row, column) position.
        Args:
            pixel: position (x, y)

        Returns:
            position (row, column)

        """
        x, y = pixel
        position = (y // self._cell_height, x // self._cell_width)
        return position

    # Same as task 1
    def get_position_center(self, position):
        """
         Gets the graphics coordinates for the center of the cell at the given (row, column) position
        Args:
            position: (row, column)

        Returns:
            (x, y)
        """
        x_min, y_min, x_max, y_max = self.get_bbox(position)
        position_center = ((x_min + x_max) / 2, (y_min + y_max) / 2)
        return position_center

    # Same as task 1
    def annotate_position(self, position, text, **kwargs):
        """
        Annotates the center of the cell at the given (row, column) position with the provided text
        Args:
            position: (row, column)
            text: string for annotation
            **kwargs:
        """
        self.create_text(self.get_position_center(position), text=text, **kwargs)


class BasicMap(AbstractGrid):
    """
    BasicMap is a view class which inherits from AbstractGrid.

    Entities are drawn on the map using coloured rectangles at different (row, column) positions.
    """
    # Same as task 1
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

    # Same as task 1
    def draw_entity(self, position, tile_type):
        """
         Draws the entity with tile type at the given position using a coloured rectangle with
         superimposed text identifying the entity
        Args:
            position: (row, col)
            tile_type: entity type, find the color in ENTITY_COLOURS

        Returns:

        """
        self.create_rectangle(self.get_bbox(position), fill=ENTITY_COLOURS[tile_type])
        self.annotate_position(position, tile_type, fill=self._entity_fg[tile_type])


class ImageMap(BasicMap):
    """
    ImageMap extends your existing BasicMap class.

    This class should behave similarly to BasicMap, except that images should be used to display each
    square rather than rectangles
    """
    def __init__(self, master, size, **kwargs):
        """
        Args:
            master:
            size:  the number of rows (= number of columns) in the grid
            **kwargs:
        """
        super().__init__(master=master, size=size, **kwargs)

        # open file as image
        image = Image.open(IMAGES[BACK_GROUND])
        image = image.resize((self._cell_width, self._cell_height)) # resize background image to given size
        self.background_img = ImageTk.PhotoImage(image)

        image = Image.open(IMAGES[PLAYER])  # Open player image
        image = image.resize((self._cell_width, self._cell_height))
        self.player_img = ImageTk.PhotoImage(image)

        image = Image.open(IMAGES[ZOMBIE])
        image = image.resize((self._cell_width, self._cell_height))
        self.zombie_img = ImageTk.PhotoImage(image)

        image = Image.open(IMAGES[HOSPITAL])
        image = image.resize((self._cell_width, self._cell_height))
        self.hospital_img = ImageTk.PhotoImage(image)

        image = Image.open(IMAGES[GARLIC])
        image = image.resize((self._cell_width, self._cell_height))
        self.garlic_img = ImageTk.PhotoImage(image)

        image = Image.open(IMAGES[CROSSBOW])
        image = image.resize((self._cell_width, self._cell_height))
        self.crossbow_img = ImageTk.PhotoImage(image)

        self.image_dict = {
            PLAYER: self.player_img,
            HOSPITAL: self.hospital_img,
            ZOMBIE: self.zombie_img,
            TRACKING_ZOMBIE: self.zombie_img,
            GARLIC: self.garlic_img,
            CROSSBOW: self.crossbow_img
        }

    def draw_background(self):
        """
        Instead of using a single image, use multiple identical background images tiled as a background
        """
        for row in range(self._rows):
            for column in range(self._cols):
                x = column * self._cell_width
                y = row * self._cell_height
                self.create_image((x, y), image=self.background_img, anchor=tk.NW)  # Show background image in x, y

    def draw_entity(self, position, tile_type, **kwargs):
        """
        Draws the entity using a image at the given position
        Args:
        position: (x, y)
        tile_type: entity type
        kwargs:
        """
        if tile_type in self.image_dict:
            self.create_image((self.get_bbox(position)[0], self.get_bbox(position)[1]), image=self.image_dict[tile_type], anchor=tk.NW)
            # Create the image within bounding position

class InventoryView(AbstractGrid):
    """
    InventoryView is a view class which inherits from AbstractGrid and displays the items the player
    has in their inventory.
    """
    # Same as task 1
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

    # Same as task 1
    def draw(self, inventory):
        """
         Draws the inventory label and current items with their remaining lifetimes
        Args:
            inventory: the player's inventory
        """
        self.delete("all")
        self.draw_label()
        for index, item in enumerate(inventory.get_items()):
            self.draw_pickup(index + 1, item, item.is_active())

    # Same as task 1
    def draw_label(self):
        """
        Draw inventory label 
        """
        x_min = 0
        y_min = 0
        x_max = self._cell_width * self._cols
        y_max = self._cell_height
        position = (x_min, y_min, x_max, y_max)
        self.create_rectangle(position, fill=LIGHT_PURPLE, outline=LIGHT_PURPLE)
        position_center = ((x_min + x_max) / 2, (y_min + y_max) / 2)
        self.create_text(position_center, text="Inventory", fill=DARK_PURPLE, font="None 14")

    # Same as task 1
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

    # Same as task 1
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


class StatusBar(tk.Frame):
    """
    a StatusBar class that inherits from tk.Frame
    """
    def __init__(self, master, **kwargs):
        """
        Args:
            master: root window
            moves_made:
            **kwargs:
        """
        self._master = master
        super().__init__(master, **kwargs)

        self._moves_made = 0
        self._timer_count = 0

        self._width = kwargs["width"]
        self._height = kwargs["height"]
        self._image_width = 40
        self._image_height = 40

        self._main_container = tk.Frame(self._master, width=self._width, height=self._height)   # Frame size
        self._main_container.pack(side=tk.TOP)

        self._chaser_frame = tk.Frame(self._main_container)
        chaser_file = "./images/chaser.png"
        chaser_img = Image.open(chaser_file)
        chaser_img = chaser_img.resize((self._image_width, self._image_height)) # Resize the photo
        chaser_img = ImageTk.PhotoImage(chaser_img) # Show the photo
        chaser_label = tk.Label(self._chaser_frame, image=chaser_img)   # Get label
        chaser_label.image = chaser_img # Label to the photo
        self._chaser_frame.pack(side=tk.LEFT)   # Where the frame is in direction and size
        chaser_label.pack(side=tk.TOP, padx=int(self._width / 30))

        self._timer_frame = tk.Frame(self._main_container)  # Create timer frame
        timer_text = tk.Label(self._timer_frame, text="Timer", font="None 10")
        minute = self._timer_count // 60
        second = self._timer_count % 60
        self._timer_count = tk.Label(self._timer_frame, text="{} mins {} seconds".format(minute, second))   # Counting format
        self._timer_frame.pack(side=tk.LEFT, padx=int(self._width / 20))   
        timer_text.pack(side=tk.TOP)
        self._timer_count.pack(side=tk.TOP)

        self._moves_frame = tk.Frame(self._main_container)
        self._moves_text = tk.Label(self._moves_frame, text="Moves made", font="None 10")   # Create how many move made
        self._moves_made = tk.Label(self._moves_frame, text="{} moves".format(self._moves_made))
        self._moves_frame.pack(side=tk.LEFT, padx=int(self._width / 20))
        self._moves_text.pack(side=tk.TOP)
        self._moves_made.pack(side=tk.TOP)

        self._button_frame = tk.Frame(self._main_container)
        self.restart_game_button = tk.Button(self._button_frame, text="Restart Game")
        self.quit_game_button = tk.Button(self._button_frame, text="Quit Game")
        self._button_frame.pack(side=tk.LEFT, padx=int(self._width / 20))
        self.restart_game_button.pack(side=tk.TOP, pady=5)
        self.quit_game_button.pack(side=tk.TOP)

        self._chasee_frame = tk.Frame(self._main_container)
        chasee_file = "./images/chasee.png"
        chasee_img = Image.open(chasee_file)
        chasee_img = chasee_img.resize((self._image_width, self._image_height))
        chasee_img = ImageTk.PhotoImage(chasee_img)
        chasee_label = tk.Label(self._chasee_frame, image=chasee_img)
        chasee_label.image = chasee_img
        self._chasee_frame.pack(side=tk.LEFT, padx=int(self._width / 30))
        chasee_label.pack(side=tk.LEFT)

    def change_time_count(self, time_count):
        """
        update the text of label
        Args:
            time
        """
        minute = time_count // 60
        second = time_count % 60
        self._timer_count.config(text="{}m {}s".format(minute, second)) # Format to count the time game play

    def change_moves_made(self, moves_made):
        """
        update the text of label
        Args:
            moves_made: new number
        """
        self._moves_made.config(text="{} moves".format(moves_made))


class ImageGraphicalInterface:
    """
    The ImageGraphicalInterface is similar to BasicGraphicalInterface
    """
    def __init__(self, root, size):
        """
        Args:
            root: the root window
            size: the number of rows (= number of columns) in the game map
        """
        self._master = root
        self._size = size
        self._game = None
        self._time_count = 0
        self._moves_made = 0
        self._timer_schedule = None
        self._step_schedule = None

        self._master.title(TITLE)

        # End of Dayz
        self._banner_width = size * CELL_SIZE + INVENTORY_WIDTH
        self._banner_height = BANNER_HEIGHT
        banner_file = "./images/banner.png"
        banner_img = Image.open(banner_file)
        banner_img = banner_img.resize((self._banner_width, self._banner_height))
        banner_img = ImageTk.PhotoImage(banner_img)

        # tk.label has attribute image, set it
        self._banner = tk.Label(self._master, image=banner_img)
        self._banner.image = banner_img
        self._banner.pack(side=tk.TOP, fill=tk.BOTH)

        # loads pictures
        self._container_width = size * CELL_SIZE + INVENTORY_WIDTH
        self._container_height = size * CELL_SIZE
        self._main_container = tk.Canvas(self._master, width=self._container_width, height=self._container_height)
        self._main_container.pack(side=tk.TOP, fill=tk.BOTH)
        self._grid = ImageMap(self._main_container, size=size)
        self._grid.pack(side=tk.LEFT)
        self._inventory = InventoryView(self._main_container, rows=size, bg=LIGHT_PURPLE)
        self._inventory.pack(side=tk.LEFT)

        # Button restart game and quit game
        self._statusbar_width = size * CELL_SIZE + INVENTORY_WIDTH
        self._statusbar_height = 10
        self._statusbar = StatusBar(self._master, width=self._statusbar_width, height=self._statusbar_height)
        self._statusbar.restart_game_button.config(command=self.restart_game)
        self._statusbar.quit_game_button.config(command=self.quit_game)
        self._statusbar.pack(side=tk.TOP)

        # parent menu
        self._menu_bar = tk.Menu(self._master)

        # What to do on each button
        self._file_menu = tk.Menu(self._menu_bar)
        self._file_menu.add_command(label="Restart game", command=self.restart_game)
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Save game", command=self.save_game)
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Load game", command=self.load_game)
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Quit", command=self.quit_game)
        self._file_menu.add_separator()
        self._file_menu.add_command(label="High scores", command=self.high_scores)

        self._master.config(menu=self._menu_bar)
        self._menu_bar.add_cascade(label="File", menu=self._file_menu)

    # Same as task 1
    def draw(self, game):
        """
        Clears and redraws the view based on the current game state.
        Args:
            game
        """
        self._grid.delete("all")
        self._grid.draw_background()
        for entity_position, tile_type in game.get_grid().get_mapping().items():
            x = entity_position.get_x()
            y = entity_position.get_y()
            self._grid.draw_entity((x, y), tile_type.display())

        self._statusbar.change_time_count(self._time_count)
        self._statusbar.change_moves_made(self._moves_made)

        inventory = game.get_player().get_inventory()
        self._inventory.draw(inventory=inventory)

        self._grid.unbind_all("<Any-KeyPress>")
        self._grid.bind_all("<Any-KeyPress>",
                            lambda event, func=self.key_press, is_fire=self.is_fire(): self.key_press(event, is_fire))

    # Same as task 1
    def key_press(self, event, is_fire):
        """
        Tap on the keyboard input
        Args:
            event
        """
        direction = event.char.upper()
        if is_fire:
            self._fire(direction)
        else:
            self._move(direction)

    # Same as task 1
    def _move(self, direction):
        """
        Handles moving the player and redrawing the game.
        Args:
            direction: direction

        """
        if direction in DIRECTIONS:
            offset = self._game.direction_to_offset(direction)
            if offset is not None:
                self._moves_made += 1
                self._game.move_player(offset)
            self.draw(self._game)

            self.stop_game()

    # Same as task 1
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

    # Same as task 1
    def is_fire(self):
        inventory = self._game.get_player().get_inventory()
        return inventory.has_active(CROSSBOW)

    # Same as task 1
    def _step(self, game):
        """
        The step method triggers the step method for the game and updates the view accordingly.

        The step method is called every second.

        Args:
            game
        """
        self._master.update()
        game.step()
        self.draw(game)

        if not self.stop_game():
            self._step_schedule = self._master.after(STEP_FPS, self._step, game)


    def _inventory_click(self, event, inventory: a2.Inventory):
        """
        This method should be called when the user left clicks on inventory view.

        It must handle activating or deactivating the clicked item (if one exists) and
        update both the model and the view accordingly.

        Args:
            event: click event
            inventory: inventory
        """
        position = (event.x, event.y)
        if self._inventory.toggle_item_activation(position, inventory):
            messagebox.showinfo(title="Alert", message="Only one item may be active at any given time!")
            return

        self._inventory.bind("<Button-1>",
                             lambda event, func=self._inventory_click, inventory=inventory: self._inventory_click(event,
                                                                                                                  inventory))

        self._grid.unbind_all("<Any-KeyPress>")
        self._grid.bind_all("<Any-KeyPress>",
                            lambda event, func=self.key_press, is_fire=self.is_fire(): self.key_press(event, is_fire))

    def timer(self):
        """
        Timer task
        """
        self._time_count = self._time_count + 1
        self._timer_schedule = self._master.after(TIME_FPS, self.timer) # Schedule the timer, every 1000

    # Same as task 1
    def play(self, game):
        """
        Binds events and initialises gameplay.
        Args:
            game
        """
        self._game = game
        self.draw(self._game)
        self.timer()
        self._step(self._game)

        inventory = game.get_player().get_inventory()
        self._inventory.bind("<Button-1>",
                             lambda event, func=self._inventory_click, inventory=inventory: self._inventory_click(event,
                                                                                                                  inventory))

        self._master.mainloop()

    def stop_schedule(self):
        """
        cancel the scheduled task
        """
        self._master.after_cancel(self._step_schedule)
        self._master.after_cancel(self._timer_schedule)

    def stop_game(self):
        """
        When to stop the game 
        """
        stop_game = False
        # Only win game and lose game will stop game
        if self._game.has_won():
            self.win_game()
            stop_game = True

        if self._game.has_lost():
            self.lose_game()
            stop_game = True

        return stop_game

    def win_game(self):
        """
        game win
        """
        self.stop_schedule()
        self._grid.unbind_all("<Any-KeyPress>")

        # Timer
        minute = self._time_count // 60 
        second = self._time_count % 60
        # Set player name if win with used time
        player_name = simpledialog.askstring(title=WIN_MESSAGE,
                                             prompt="You won in {}m and {}s! Enter your name:".format(minute, second))
        try:
            with open(HIGH_SCORES_FILE) as record_file: # Open a file to store highest score
                records = record_file.readlines() 
        except IOError:
            open(HIGH_SCORES_FILE, "w+").close()
            records = []

        records_sorted = []
        for record in records:
            record = record.strip("\n").split(",")  # Sort out every record with newline and commar
            records_sorted.append((str(record[0]), strtotime(record[1])))

        records_sorted.append((player_name, self._time_count))
        records_sorted = sorted(records_sorted, key=lambda x: x[1])[:MAX_ALLOWED_HIGH_SCORES:]
        with open(HIGH_SCORES_FILE, "w") as file:
            file.write("".join("{},{}\n".format(x[0], timetostr(x[1])) for x in records_sorted))

        if messagebox.askyesno(title=WIN_MESSAGE, message="Would you like to play again?"):
            self.restart_game()

    def lose_game(self):
        """
        after the game lost
        Returns:

        """
        self.stop_schedule()
        if messagebox.askyesno(title=LOSE_MESSAGE, message="Would you like to play again?"):
            self.restart_game()

    def quit_game(self):
        if messagebox.askyesno(title="Quit Game?", message="Are you sure you want to quit?"):
            self._master.destroy()

    def restart_game(self):
        """
        start a new game
        Returns:

        """
        self._grid.delete("all")
        self.stop_schedule()
        self._game = a2.advanced_game(MAP_FILE)
        self._moves_made = 0
        self._time_count = 0
        self.play(self._game)

    def save_game(self):
        """
        save game to file

        Returns:

        """
        try:
            self.stop_schedule()
            self._grid.unbind_all("<Any-KeyPress>")

            filename = filedialog.asksaveasfilename(title="Save Game", defaultextension=".txt")

            save_information = [self._time_count, self._moves_made]

            temp_dict = {}
            inventory = self._game.get_player().get_inventory()
            for pickup in inventory.get_items():
                temp_dict.update({pickup.display(): pickup.get_lifetime()})
            inventories = str(temp_dict)
            save_information.append(inventories)

            temp_dict.clear()
            maps = self._game.get_grid().get_mapping()
            for position, entity in maps.items():
                temp_dict.update({(position.get_x(), position.get_y()): entity.display()})

            maps = ""
            for y in range(self._size):
                for x in range(self._size):
                    if temp_dict.get((x, y)):
                        maps = "".join([maps, temp_dict.get((x, y))])
                    else:
                        maps = "".join([maps, " "])
                maps += "\n"

            save_information.append(maps)

            with open(filename, "w") as file:
                for item in save_information:
                    file.write("{}\n".format(item))
        except Exception as e:
            print(e)
            pass

    def load_game(self):
        """
        Returns:

        """
        try:
            self.stop_schedule()
            filename = filedialog.askopenfilename()
            with open(filename) as game_file:
                game_information = game_file.readlines()

            grid_information = ""
            extra_information = ""
            for index, line in enumerate(game_information):
                if index == 0:
                    extra_information = "".join([extra_information, line])
                    self._time_count = int(line.strip("\n"))
                elif index == 1:
                    extra_information = "".join([extra_information, line])
                    self._moves_made = int(line.strip("\n"))
                elif index == 2:
                    extra_information = "".join([extra_information, line])
                    inventory = eval(line.strip("\n"))
                else:
                    grid_information = "".join([grid_information, line])

            with open(filename, "w") as map_file:
                map_file.write(grid_information)

            self._game = a2.advanced_game(filename)
            for tile_type, lifetime in inventory.items():
                if tile_type is GARLIC:
                    pickup = a2.Garlic()
                if tile_type is CROSSBOW:
                    pickup = a2.Crossbow()
                pickup.set_lifetime(lifetime=lifetime)
                self._game.get_player().get_inventory().add_item(pickup)

            with open(filename, "w+") as origin_file:
                origin_file.write(extra_information + grid_information)

            self.play(self._game)
        except Exception as e:
            print(e)
            pass

    def high_scores(self):
        """
        Selecting this option should create a top level window displaying an ordered leaderboard
        of the best time achieved by users in the game
        Returns:

        """
        high_scores_widget = tk.Toplevel(self._master)
        title = tk.Label(high_scores_widget, text="High Scores", fg=WHITE, font="None 16 bold", bg=DARKEST_PURPLE)
        high_scores_widget.title("Top 3")
        title.pack(side=tk.TOP, fill=tk.BOTH)

        try:
            with open(HIGH_SCORES_FILE) as record_file:
                records = record_file.readlines()
        except IOError:
            open(HIGH_SCORES_FILE, "w+").close()
            records = []

        records_sorted = []
        for record in records:
            record = record.strip("\n").split(",")
            records_sorted.append((str(record[0]), record[1]))

        try:
            first = tk.Label(high_scores_widget, text="{}: {}".format(records_sorted[0][0], records_sorted[0][1]))
            first.pack(side=tk.TOP)
            second = tk.Label(high_scores_widget, text="{}: {}".format(records_sorted[1][0], records_sorted[1][1]))
            second.pack(side=tk.TOP)
            third = tk.Label(high_scores_widget, text="{}: {}".format(records_sorted[2][0], records_sorted[2][1]))
            third.pack()
        except Exception as e:
            pass
        done_button = tk.Button(high_scores_widget, text="Done", command=high_scores_widget.destroy)
        done_button.pack(side=tk.TOP)


def strtotime(time_str):
    if len(time_str.split("m")) > 1:
        minute = time_str.split("m")[0]
        second = time_str.split("m")[1].strip("s\n")
    else:
        minute = 0
        second = time_str.strip("s\n")
    return 60 * int(minute) + int(second)


def timetostr(time):
    minute = time // 60
    second = time % 60
    if minute > 0:
        time_str = ("{}m {}s".format(minute, second))
    else:
        time_str = ("{}s".format(second))
    return time_str

