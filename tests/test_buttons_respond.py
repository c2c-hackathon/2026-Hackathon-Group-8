"""Component tests for Connect Four button presses that should be accepted."""

import pytest
import unittest.mock


def test___new_game___column_pressed___piece_drops_to_bottom_row(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    original_color = board.color_at(0, 7)

    board.press(0, 0)

    assert board.color_at(0, 6) == original_color
    assert board.color_at(0, 7) != original_color


def test___new_game___column_pressed_twice___pieces_stack_and_turn_indicator_alternates(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    original_color = board.color_at(0, 7)

    board.press(3, 0)

    assert board.color_at(3, 6) == original_color
    assert board.color_at(3, 7) != original_color


def test___game_with_one_piece___column_pressed___piece_drops_to_next_row_and_turn_indicator_alternates(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board
    original_color = board.color_at(0, 7)
    board.press(3, 0)  # Player 1's turn, tested above, now Player 2's turn
    player_one_color = board.color_at(0, 7)

    board.press(3, 0)

    assert board.color_at(3, 5) == original_color
    assert board.color_at(3, 6) != original_color
    assert board.color_at(3, 6) != player_one_color
