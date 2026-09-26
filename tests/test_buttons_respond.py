"""Component tests for Connect Four button presses that should be accepted."""

import pytest
import unittest.mock


def test___new_game___column_pressed___piece_drops_to_bottom_row(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    board.press(0, 0)

    assert board.color_at(0, 7) == game.get_player_color(connect_four_module.CellState.PLAYER_1)
    assert board.color_at(0, 6) == game.get_player_color(connect_four_module.CellState.EMPTY)


@pytest.mark.parametrize("y", [1, 2, 3, 4, 5, 6])
def test___new_game___button_not_in_top_row_pressed___nothing_happens(
    y,
    connect_four_module,
    game_and_board,
):
    _game, board = game_and_board
    board.set_cell_color = unittest.mock.Mock()

    board.press(0, y)

    board.set_cell_color.assert_not_called()


def test___new_game___column_pressed_twice___pieces_stack_and_turn_indicator_alternates(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    board.press(3, 0)

    assert board.color_at(3, 7) == game.get_player_color(connect_four_module.CellState.PLAYER_1)
    assert board.color_at(0, 0) == game.get_player_color(connect_four_module.CellState.PLAYER_2)


def test___game_with_one_piece___column_pressed___piece_drops_to_next_row_and_turn_indicator_alternates(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    board.press(3, 0)  # Player 1's turn, tested above, now Player 2's turn

    board.press(3, 0)

    assert board.color_at(3, 6) == game.get_player_color(connect_four_module.CellState.PLAYER_2)
    assert board.color_at(0, 0) == game.get_player_color(connect_four_module.CellState.PLAYER_1)
