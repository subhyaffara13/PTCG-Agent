
def compute_reward(player):
    ct_count = sum([len(v.citytiles) for k, v in player.cities.items()])
    unit_count = len(game_state.players[player.team].units)
    # max board size is 32 x 32 => 1024 max city tiles and units, so this should keep it strictly so we break by city tiles then unit count
    return ct_count * 10000 + unit_count

