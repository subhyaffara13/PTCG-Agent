
def _make_game_info(params):
  """Create game info based on parameters."""
  num_ants = params.get("num_ants", _DEFAULT_PARAMS["num_ants"])
  num_food = params.get("num_food", _DEFAULT_PARAMS["num_food"])
  max_turns = params.get("max_turns", _DEFAULT_PARAMS["max_turns"])
  return pyspiel.GameInfo(
      num_distinct_actions=_NUM_ACTIONS,
      max_chance_outcomes=0,
      num_players=num_ants,
      min_utility=0.0,
      max_utility=float(num_food),
      utility_sum=None,  # Not constant sum
      max_game_length=max_turns * num_ants,
  )

