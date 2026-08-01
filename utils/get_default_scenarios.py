
def get_default_scenarios(game_name):
  """Loads the default scenarios for a given game.

  Args:
    game_name: The game to load scenarios for.

  Returns:
    A List[Scenario] detailing the scenarios for that game.
  """
  return SCENARIOS[game_name]

