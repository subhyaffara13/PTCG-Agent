
def evaluate_state(state: pyspiel.State, player: int):
  """Evaluates the given state for the specified player.

  Args:
    state: The state to evaluate.
    player: The player to evaluate for.

  Returns:
    The heuristic value of the state for the specified player. A higher value
    means the state is better for the specified player.
  """
  game_str = state.get_game().get_type().short_name
  if game_str not in HEURISTIC_CALLBACKS:
    raise ValueError(f"No heuristic callback found for game {game_str}.")
  return HEURISTIC_CALLBACKS[game_str](state, player)

