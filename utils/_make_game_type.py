
def _make_game_type(params):
  """Create the game type with the given parameters."""
  num_ants = params.get("num_ants", _DEFAULT_PARAMS["num_ants"])
  return pyspiel.GameType(
      short_name="python_ant_foraging",
      long_name="Python Ant Foraging",
      dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
      chance_mode=pyspiel.GameType.ChanceMode.DETERMINISTIC,
      information=pyspiel.GameType.Information.PERFECT_INFORMATION,
      utility=pyspiel.GameType.Utility.IDENTICAL,
      reward_model=pyspiel.GameType.RewardModel.TERMINAL,
      max_num_players=num_ants,
      min_num_players=num_ants,
      provides_information_state_string=True,
      provides_information_state_tensor=False,
      provides_observation_string=True,
      provides_observation_tensor=True,
      parameter_specification={},
  )

