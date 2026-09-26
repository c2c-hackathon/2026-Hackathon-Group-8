"""Component tests for Connect Four presses that should be rejected."""


def test___column_is_full___same_column_pressed___extra_move_is_rejected(game_and_board):
    game, board = game_and_board
    for _ in range(6):
        assert board.press(0, 0)
    colors_before_extra_press = dict(board.colors)

    accepted = board.press(0, 0)

    assert not accepted
    assert board.key_states[(0, 0)]["enable"] is False
    assert board.colors == colors_before_extra_press

def test___column_is_full___same_column_pressed___turn_indicator_stays_on_current_player(
    connect_four_module,
    game_and_board,
):
    game, board = game_and_board

    for _ in range(6):
        board.press(0, 0)

    indicator_color_before_extra_press = board.color_at(1, 0)
    player_colors = {
        game.get_player_color(connect_four_module.CellState.PLAYER_1),
        game.get_player_color(connect_four_module.CellState.PLAYER_2),
    }

    board.press(0, 0)

    assert indicator_color_before_extra_press in player_colors
    assert board.color_at(1, 0) == indicator_color_before_extra_press
