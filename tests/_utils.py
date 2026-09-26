def player_state(connect_four_module, player_token):
    if player_token == "1":
        return connect_four_module.CellState.PLAYER_1
    return connect_four_module.CellState.PLAYER_2
