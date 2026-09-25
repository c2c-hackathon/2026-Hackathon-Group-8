import abc
import typing
import enum

import board

import busio
import digitalio
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis
import pygame.mixer
import os


class Action(enum.IntEnum):
    """
    Options for what button action to respond to.
    """
    BUTTON_PRESSED = NeoTrellis.EDGE_RISING
    BUTTON_RELEASED = NeoTrellis.EDGE_FALLING

class AbstractNeoTrellisGame(abc.ABC):
    @abc.abstractmethod
    def init_hardware(self):
        """Initializes the LED board."""
        pass

    @abc.abstractmethod
    def set_cell_color(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        """Sets the color of a cell at the given coordinates."""
        pass

    @abc.abstractmethod
    def update_display(self):
        """Updates the LED display to reflect any changes made to cell colors."""
        pass

    @abc.abstractmethod
    def clear_board(self):
        """Clears board by turning off all LEDs"""
        pass

    @abc.abstractmethod
    def sync(self):
        """Read any events from the LED display and call callbacks if any events have occurred."""
        pass

    @abc.abstractmethod
    def set_callback(self, x: int, y: int, callback) -> None:
        """Sets a callback function for a cell at the given coordinates."""
        pass

    @abc.abstractmethod
    def activate_key(self, x: int, y: int, action: Action, enable: typing.Optional[bool] = True) -> None:
        """Activates a key at the given coordinates for a specific action."""
        pass


class NeoTrellisGame(AbstractNeoTrellisGame):
    """
    DO NOT MODIFY!!!! >:(
    """
    
    def __init__(self):
        self._board = None
        pygame.mixer.init()
        self.init_hardware()
        self._sounds = {}

    def init_hardware(self):
        """
        NOTE: This is called already in the NeoTrellisGame.__init__(), you should not need to call it explicitly.
        Setup the hardware communication. This function is called upon creation of a NeoTrellisGame, and must be called prior to using any other method that interacts with the hardware.
        """
        print("Initializing Hardware")
        i2c_bus = busio.I2C(board.SCL, board.SDA)

        self.__boards = [
            [NeoTrellis(i2c_bus, False, addr=0x2E, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x2F, auto_write=False)],
            [NeoTrellis(i2c_bus, False, addr=0x30, auto_write=False), NeoTrellis(i2c_bus, False, addr=0x31, auto_write=False)],
            ]
        self._board = MultiTrellis(self.__boards)
        print("Hardware is ready")
    
    def validate_coordinates(self, x: int, y: int):
        """
        Validate the given coordinates are within bounds.

        Both X and Y can range from [0, 7] inclusive. 
        If either the X or Y coordinate is out of bounds a ValueError will be raised indicating the incorrect coordinate.

        Parameters
        ----------
        x: int
            The X coordinate to convert.
        y: int
            The Y coordinate to convert.
        
        Returns
        -------
        int
            An integer representing the index of the key pressed

        Raises
        ------
        ValueError
            When either the X or Y coordinate is out of bounds.

        """
        if x < 0 or x > 7:
            raise ValueError(f"X coordinate must be between 0 and 7 inclusive. Was {x}") 
        
        if y < 0 or y > 7:
            raise ValueError(f"Y coordinate must be between 0 and 7 inclusive. Was {y}") 
    
    def set_cell_color(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        """
        Set the cell light to an RGB color. This color will not be shown until update_display() is called. 

        Both X and Y can range from [0, 7] inclusive.
        Each value of the RGB color can range from [0, 255] inclusive.

        Parameters
        ----------
        x: int
            The X coordinate of the cell to change.
        y: int
            The Y coordinate of the cell to change.
        color: tuple[int, int, int]
            A tuple containing the RGB value to set the cell to.

        Raises
        ------
        ValueError
            When the X or Y coordinate is outside its valid range [0, 7] inclusive, 
            or when an R, G, or B value is outside its valid range [0, 255] inclusive.
        """
        self.validate_coordinates(x, y)
        for rgbValue in color:
            if rgbValue < 0 or rgbValue > 255:
                raise ValueError(f"All RGB values in the color must be between 0 and 255 inclusive. Was {color}")
        self._board.color(x, y, color)
    
    def update_display(self):
        """
        Update the display to show all cell colors.

        The colors can be set through set_cell_color(), however no changes will be displayed until this method is called.
        
        """
        self._board.show()

    def clear_board(self):
        """
        Clears the board by setting all cell lights to the color (0,0,0) and calling update_display()
        """
        for x in range(8):
            for y in range(8):
                self.set_cell_color(x, y, (0, 0, 0))
        self.update_display()

    def sync(self):
        """
        NOTE: You should not need to explicity call this method in your solution as it is called in main.py

        Read all board events and call any callbacks associated with them. 
        """
        self._board.sync()

    def set_callback(self, x: int, y: int, callback) -> None:
        """
        Configures the function that will run when a button at coordinates x and y is pressed/released. 
        
        The function must accept three parameters x, y, and action. X and Y will represent the x and y coordinates of the button when the function is called, and the action will indicate whether the button was pressed or released. 
        Use the Action.BUTTON_PRESSED and Action.BUTTON_RELEASED constants defined at the top of the file to specify the action.
        
        An example callback function would have the definition of my_callback(x, y, action) and would be set by calling set_callback(x, y, my_callback)
        If the callback function is a member of a class, then the definition would look like my_callback(self, x, y, action) and would be set by calling set_callback(x, y, self.my_callback)

        Parameters
        ----------
        x: int
            The X coordinate of the key to set the callback on.
        y: int
            The Y coordinate of the key to set the callback on.
        callback: function
            The function to call when the key is pressed.
        """
        self._board.set_callback(x, y, callback)

    def activate_key(self, x: int, y: int, action, enable=True) -> None:
        """
        Activates the key to start listening button presses and releases. The optional parameter 'enable' allows toggling the key on and off. The default value of True will enable the key, where setting it to false will disable the key.
        The action can be one of the following:
        Action.BUTTON_PRESSED - Calls the callback (function) when the button is pressed
        Action.BUTTON_RELEASED - Calls the callback (function) when the button is released

        Parameters
        ----------
        x: int
            The X coordinate of the key to activate or deactivate.
        y: int
            The Y coordinate of the key to activate or deactivate.
        action: Action
            The action specifying when the callback should be run.
        enable: bool
            Whether to enable or disable the key.
        """
        self._board.activate_key(x, y, action, enable)
    
    def clear_keypad_buffer(self):
        """
        NOTE: This function is not required, but may be useful in implementing bonus features!
        Clears the buffer of key events. This ensures that button presses on disabled keys will not be handled even when the key is re-enabled.
        """
        for row in self.__boards:
            for trel in row:
                trel.read_keypad(trel.count)

    def play_sound(self, sound_name, extra_plays=0):
        """
        Plays a sound, with an option to repeat the after the original play. The sound name should refer to a file in the sounds folder. 
        """
        sound_to_play = None
        try:
            sound_to_play = self.sounds[sound_name]
        except:
            sound_to_play = pygame.mixer.Sound(os.path.join("sounds", sound_name))
            self._sounds[sound_name] = sound_to_play
        sound_to_play.play(loops=extra_plays)

    def stop_sound(self, sound_name):
        """
        Stops playing a sound if it is playing. The sound name should refer to a file in the sounds folder. 
        """
        try: 
            self._sounds[sound_name].stop()
        except Exception:
            pass

