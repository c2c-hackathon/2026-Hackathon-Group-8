"""Component tests for Connect Four win and tie detection."""

import pytest

# board state:
# [
#     "........",
#     "........",
#     "........",
#     "P......F",
#     "P......F",
#     "P......F",
# ]
VERTICAL_FIRST_COLUMN_MOVES = [0, 7, 0, 7, 0, 7]

# board state:
# [
#     "........",
#     "........",
#     "........",
#     "...FP...",
#     "...FP...",
#     "...FP...",
# ]
VERTICAL_MIDDLE_COLUMN_MOVES = [4, 3, 4, 3, 4, 3]

# board state:
# [
#     "........",
#     "........",
#     "........",
#     "........",
#     "........",
#     "PPP..FFF",
# ]
HORIZONTAL_BOTTOM_ROW_MOVES = [2, 7, 1, 6, 0, 5]

# board state:
# [
#     "........",
#     "........",
#     "........",
#     "..PPP...",
#     ".FFPFP..",
#     "FFPFPF..",
# ]
HORIZONTAL_MIDDLE_ROW_MOVES = [4, 5, 5, 4, 4, 3, 2, 2, 3, 1, 3, 1, 2, 0]

# board state:
# [
#     "PPFFPPF.",
#     "FFPPFFPP",
#     "PPFFPPFF",
#     "FFPPFFPP",
#     "PPFFPPFF",
#     "FFPPFFPP",
# ]
TIE_MOVES = [7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 7, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 4, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]


def replay_moves(connect_four_module, board, moves):
    board.PRESS_DELAY_SECONDS = 0

    for column in moves:
        assert board.press(column, 0)

    if len(moves) % 2 == 0:
        return connect_four_module.CellState.PLAYER_1
    return connect_four_module.CellState.PLAYER_2


def assert_game_is_active(connect_four_module, board):
    for column in range(7):
        assert board.color_at(column, 0) != (0, 0, 0)

    assert board.callbacks[(7, 0)] is not None


def assert_end_game_controls(connect_four_module, board):
    for column in range(7):
        assert board.color_at(column, 0) == (0, 0, 0)

    assert board.callbacks[(7, 0)] is not None
    assert board.color_at(7, 0) == connect_four_module.HIGHLIGHT_COLOR


def test___three_pieces_in_first_column___column_pressed___vertical_win_is_detected(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    current_player = replay_moves(connect_four_module, board, VERTICAL_FIRST_COLUMN_MOVES)

    board.press(0, 0)

    assert board.color_at(0, 4) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


def test___three_pieces_in_last_column___column_pressed___vertical_win_is_detected(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    replay_moves(connect_four_module, board, VERTICAL_FIRST_COLUMN_MOVES)
    board.press(1, 0)  # player 1 misses, player 2's turn

    board.press(7, 0)

    assert board.color_at(7, 4) == game.get_player_color(connect_four_module.CellState.PLAYER_2)
    assert_end_game_controls(connect_four_module, board)


def test___three_pieces_in_middle_column___column_pressed___vertical_win_is_detected(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    current_player = replay_moves(connect_four_module, board, VERTICAL_MIDDLE_COLUMN_MOVES)

    board.press(4, 0)

    assert board.color_at(4, 4) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


def test___three_bottom_row_pieces___adjacent_column_pressed___horizontal_bottom_row_win_is_detected(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    current_player = replay_moves(connect_four_module, board, HORIZONTAL_BOTTOM_ROW_MOVES)

    board.press(3, 0)

    assert board.color_at(3, 7) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


def test___three_middle_row_pieces___supported_column_pressed___horizontal_middle_row_win_is_detected(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    current_player = replay_moves(connect_four_module, board, HORIZONTAL_MIDDLE_ROW_MOVES)

    board.press(5, 0)

    assert board.color_at(5, 5) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


DIAGONAL_CASES = [
    pytest.param(
        # board state:
        # [
        #     "........",
        #     "........",
        #     "........",
        #     "FP......",
        #     "FFP.....",
        #     "FPFP...P",
        # ]
        [7, 2, 1, 1, 3, 0, 2, 0, 1, 0],
        0,
        2,
        0,
        id="descending-left-edge",
    ),
    pytest.param(
        # board state:
        # [
        #     "........",
        #     "........",
        #     "........",
        #     "..PF...P",
        #     ".PFF...P",
        #     "PFFF...P",
        # ]
        [7, 3, 7, 2, 6, 2, 2, 1, 1, 3, 0, 3],
        3,
        2,
        3,
        id="ascending-left-edge",
    ),
    pytest.param(
        # board state:
        # [
        #     "........",
        #     "........",
        #     "........",
        #     "..FP...P",
        #     "..FFP..P",
        #     "..FFFP.P",
        # ]
        [7, 4, 7, 3, 7, 3, 5, 2, 4, 2, 3, 2],
        2,
        2,
        2,
        id="descending-middle",
    ),
    pytest.param(
        # board state:
        # [
        #   "........",
        #   "........",
        #   "........",
        #   "....FP..",
        #   "....PFP.",
        #   "P...FFFP",
        # ]
        [7, 6, 6, 5, 0, 5, 5, 4, 4, 4],
        4,
        2,
        4,
        id="descending-right-edge",
    ),
    pytest.param(
        # Foe wins case
        # board state:
        # [
        #     "........",
        #     "........",
        #     "....P...",
        #     "...PFF.P",
        #     "P.PFFF.P",
        #     "P.FFFP.P",
        # ]
        [7, 4, 7, 4, 7, 4, 5, 3, 4, 3, 3, 2, 2, 5, 0, 5, 0],
        5,
        2,
        5,
        id="ascending-middle",
    ),
]


@pytest.mark.parametrize("moves, move_column, expected_row, expected_column", DIAGONAL_CASES)
def test___three_diagonal_pieces___supported_column_pressed___diagonal_win_is_detected(
    connect_four_module,
    game_and_board,
    moves,
    move_column,
    expected_row,
    expected_column,
):
    game, board = game_and_board
    current_player = replay_moves(connect_four_module, board, moves)
    assert_game_is_active(connect_four_module, board)

    board.press(move_column, 0)

    assert board.color_at(
        expected_column, expected_row + connect_four_module.ROW_OFFSET
    ) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)


def test___board_has_one_empty_cell_without_a_winner___final_column_pressed___tie_is_detected(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    current_player = replay_moves(connect_four_module, board, TIE_MOVES)

    board.press(7, 0)

    assert board.color_at(7, 2) == game.get_player_color(current_player)
    assert_end_game_controls(connect_four_module, board)
