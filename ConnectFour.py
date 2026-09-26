import typing

from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis
import Colors

class ConnectFour:

    def tickCallback(self):
        new_list = []
        self.update_board_colors()
        for i, falling_cell in enumerate(self.falling_cells):
            print("falling cell")
            player = falling_cell[0]
            col = falling_cell[1]
            row = falling_cell[2]
            # draw falling cell
            self.board.set_cell_color(col, row, self.get_player_color(player))

            falling_cell[2] += 1
            if self.find_lowest_empty_row(col) == -1:
                continue
            if falling_cell[2] != self.find_lowest_empty_row(col)+2:
                new_list.append(falling_cell)
            else:
                self.place_piece(col, player)

        self.falling_cells = new_list

        self.board.update_display()


    def __init__(self, board: typing.Optional[AbstractNeoTrellisGame] = None):
        self.board = board if board is not None else NeoTrellisGame(self.tickCallback)
        super().__init__()
        self.register_callbacks()
        # 6x8 matrix, 0 = empty, 1 = player 1, 2 = player 2
        self.game_state = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.falling_cells = [] # list of falling cells, each falling cell is [player, col, row]
        print(self.game_state)
        # current player: 1 or 2
        self.player = 1
        on = True
        self.register_callbacks()

        if on == True:
            for r in range(0,8):
                for c in range(2,8):
                    self.board.set_cell_color(r,c,Colors.WHITE)
            self.board.set_cell_color(7,1,Colors.ORANGE)
            
        elif on == False:
            self.board.clear_board()
            

        self.show_current_player()

    def reset_game(self):
        #TODO reset the game state to its original empty state
        self.game_state = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.player = 1
        

    def register_callbacks(self):
        #TODO: Register callbacks that will be run when buttons are pressed and released
        for i in range(8):
            for j in range(8):
                self.board.activate_key(i, j, Action.BUTTON_PRESSED, True) # Even though the callback is set, if the key is not enabled it will not be run. This is how you enable

                self.board.set_callback(i, j, self.handle_button_event) # Example of how to register a callback (function) for button 0, 0. Must be done for every button that runs a function
  
    def handle_button_event(self, x:int, y: int, action: Action):
        """
        This is an example of how a callback function will look. It takes an x value, y value, and action, which will indicate what button activated the callback and what action the user did to run it.
        See NeoTrellisGame.set_callback() for info about callbacks.
        """
        # print(f"Pressed [{x}, {y}]")
        #TODO: Implement what will happen when the button at position x,y is pressed or released
        if y == 0:
            print(f"player: {self.player}")
            if self.find_lowest_empty_row(x) != -1:
                self.drop_piece(x)

        if x == 7 and y == 1:
            print("RESET GAME")
            self.board.play_sound("ding.mp3")
            self.reset_game()


        self.show_current_player()
        self.update_board_colors()
        self.board.update_display()
        self.show_winner()
        self.show_tie_game()

    def find_lowest_empty_row(self, col: int):
        # Return the lowest empty row in the column.
        for i in range(6):
            if self.game_state[i][col] != 0:
                return i - 1
        return 5
    
    def drop_piece(self, col: int):
        
        self.falling_cells.append([self.player, col, 0])
        self.switch_player()

    def place_piece(self, col: int, player: int):
        #TODO: Finds the legal move in the column, and updates the game state to reflect the new piece, checking to see if a player has won with that new piece. Don't forget to play a sound!
        row = self.find_lowest_empty_row(col)
        if row == -1:
            self.board.play_sound("error.mp3")
            return
        print(f"The row is {row} and column is {col}")
        self.game_state[row][col] = player
        self.board.play_sound("clack.mp3")
        # print(self.game_state)
        self.check_win()
        print("WIN" if self.check_win() != False else "")
    

    def update_board_colors(self):
        self.show_current_player()
        for c in range(7):
            self.board.set_cell_color(c, 1, (0, 0, 0))
        self.board.set_cell_color(7,1,Colors.ORANGE)
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        for r in range(6):
            for c in range(8):
                play_set_color = self.get_player_color(self.game_state[r][c])
                self.board.set_cell_color(c,r+2,play_set_color)


    def switch_player(self):
        # Change which player is curently placing a piece. Keep track of this in some sort of variable
        self.player = 1 if self.player == 2 else 2

    def show_current_player(self):
        #TODO: Function to indicate on the board which player is currently placing a piece
        for i in range(8):
            self.board.set_cell_color(i,0,self.get_player_color(self.player))

    def is_board_full(self):
        # Return whether or not the game state has no more legal moves
        for i in range(6):
            for j in range(8):
                if self.game_state[i][j] == 0:
                    return False
        return True
        

    def get_player_color(self, player) -> tuple[int, int, int]:
        # Return the color for the given player 
        if player == 0:
            return Colors.WHITE
        elif player == 1:
            return Colors.GREEN
        else:
            return Colors.RED

    def is_column_full(self, col: int):
        # Return if the given column is currently full
        for i in range(6):
            if self.game_state[i][col] == 0:
                return False
        return True


    def check_win(self):
        #TODO: Check the game state to see if any player has won or if there is a draw
        # Check rows, columns, and diagonals for a win
        for row in range(6):
            for column in range(8):
                if self.game_state[row][column] != 0:
                    #Check for a win in the column
                    if row <= 2:
                        #Checking the column for a win by iterating through the rows below
                        if (self.game_state[row][column] == self.game_state[row+1][column] == self.game_state[row+2][column] == self.game_state[row+3][column]):
                            print(self.game_state[row][column])
                            print(self.game_state[row+1][column])
                            print(self.game_state[row+2][column])
                            print(self.game_state[row+3][column])
                            # A win has been found in the column
                            return [self.game_state[row][column],row,column]
                            
                        

        # Check for a win in the row
        for row in range(6):
            for column in range(8):
                if self.game_state[row][column] != 0:
                    if column >= 3 and column <= 4:
                        if (self.game_state[row][column] == self.game_state[row][column+1] == self.game_state[row][column+2] == self.game_state[row][column+3]):
                            # A win has been found in the row
                            return [self.game_state[row][column],row,column]

        # Check for a win in the diagonals from left to right
        for row in range(6):
            for column in range(8):
                if self.game_state[row][column] != 0:
                    if column <= 4 and row <= 2:
                        if (self.game_state[row][column] == self.game_state[row+1][column+1] == self.game_state[row+2][column+2] == self.game_state[row+3][column+3]):
                            return [self.game_state[row][column],row,column] 

        # Check for a win in the diagonals from right to left
        for row in range(6):
                    for column in range(8):
                        if self.game_state[row][column] != 0:
                            if column >= 4 and row <= 2:
                                if (self.game_state[row][column] == self.game_state[row+1][column-1] == self.game_state[row+2][column-2] == self.game_state[row+3][column-3]):
                                    return [self.game_state[row][column],row,column]
        return False
    
    def show_winner(self):
        #TODO: Display on the board who won
        if self.check_win() != False:
             self.board.play_sound("cheer.mp3")

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        if self.is_board_full() and self.check_win() != False:
             self.board.play_sound("aww.mp3")



