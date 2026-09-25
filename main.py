import time

from ConnectFour import ConnectFour

connect_four = ConnectFour()
connect_four.board.update_display()
while True:
    try:
        connect_four.board.sync()
        time.sleep(0.1)
    except KeyboardInterrupt:
        # clear board
        print("\nClosing game...")
        connect_four.board.clear_board()
        exit()  # quit

