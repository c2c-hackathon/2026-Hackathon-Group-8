import typing

from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis

class ConnectFour:
    def __init__(self, board: typing.Optional[AbstractNeoTrellisGame] = None):
        self.board = board if board is not None else NeoTrellisGame()
        super().__init__()
        # 6x8 matrix, 0 = empty, 1 = player 1, 2 = player 2
        self.game_state = [[0, 0, 0, 0, 0, 0, 0, 0]*6]
        # current player: 1 or 2
        self.player = 1

    def reset_game(self):
        #TODO reset the game state to its original empty state
        self.game_state = [[0, 0, 0, 0, 0, 0, 0, 0]*6]
        pass

    def register_callbacks(self):
        #TODO: Register callbacks that will be run when buttons are pressed and released
        self.board.set_callback(0, 0, self.handle_button_event) # Example of how to register a callback (function) for button 0, 0. Must be done for every button that runs a function
        self.board.activate_key(0, 0, Action.BUTTON_PRESSED) # Even though the callback is set, if the key is not enabled it will not be run. This is how you enable

        pass
  
    def handle_button_event(self, x:int, y: int, action: Action):
        """
        This is an example of how a callback function will look. It takes an x value, y value, and action, which will indicate what button activated the callback and what action the user did to run it.
        See NeoTrellisGame.set_callback() for info about callbacks.
        """
        #TODO: Implement what will happen when the button at position x,y is pressed or released
        if y == 0:
            place_piece(x)

    def find_lowest_empty_row(self, col: int):
        # Return the lowest empty row in the column.
        for i in range(6):
            if self.game_state[i][col] != 0:
                return i - 1
        return 7

    def place_piece(self, col: int):
        #TODO: Finds the legal move in the column, and updates the game state to reflect the new piece, checking to see if a player has won with that new piece. Don't forget to play a sound!
        row = find_lowest_empty_row(col)
        self.game_state[row][col] = self.player
        pass

    def update_board_colors(self):
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        pass

    def switch_player(self):
        # Change which player is curently placing a piece. Keep track of this in some sort of variable
        self.player = 1 if player == 2 else 2

    def show_current_player(self):
        #TODO: Function to indicate on the board which player is currently placing a piece
        pass

    def is_board_full(self):
        #TODO: Return whether or not the game state has no more legal moves
        pass

    def get_player_color(self, player) -> tuple[int, int, int]:
        # Return the color for the given player 
        return Colors.GREEN if player == 0 else Colors.RED

    def is_column_full(self, col: int):
        # Return if the given column is currently full
        for i in range(6):
            if self.game_state[col][i] == 0:
                return False
        return True

    def check_win(self):
        #TODO: Check the game state to see if any player has won or if there is a draw
        pass

    def show_winner(self):
        #TODO: Display on the board who won
        pass

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        pass


