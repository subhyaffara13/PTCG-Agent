
def _update_observations(state, game, action_log=None):
    """Serialise the current GameState into each agent's observation.

    ``action_log`` is the slice of ``game.action_history`` produced during
    the turn just processed (engine-side records: damage, kills, evade,
    bonus flags, tile HP/owner after seize, etc.). It's mirrored to both
    agents' observations so replays carry the engine's self-describing
    outcomes instead of only the agent's raw submitted actions.
    """
    board = _serialize_board(game)
    structures = _serialize_structures(game)
    gold = [game.player_gold.get(1, 0), game.player_gold.get(2, 0)]
    units = _serialize_units(game)
    log = action_log if action_log is not None else []

    for i in range(2):
        obs = state[i].observation
        obs.board = board
        obs.structures = structures
        obs.gold = gold
        obs.units = units
        obs.turnNumber = game.turn_number
        obs.mapWidth = game.grid.width
        obs.mapHeight = game.grid.height
        obs.actionLog = log

