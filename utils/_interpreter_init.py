
def _interpreter_init(state, env, key):
    """Handle the first interpreter call (game initialisation)."""
    seed = _resolve_seed(env)
    game = _init_game(env.configuration, seed)
    _games[key] = game
    _update_observations(state, game)
    state[0].status = "ACTIVE"
    state[1].status = "INACTIVE"
    return state

