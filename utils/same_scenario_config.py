
def same_scenario_config(
    config: ml_collections.config_dict.ConfigDict,
    game_id: int,
) -> ml_collections.config_dict.ConfigDict:
  """Dummy function for games that don't need any config modification.

  Arguments:
    config: the original game scenario config dict (this should contain
      examples for generating new scenarios)
    game_id: int, unused
  Returns:
    new_config: original game config
  """
  del game_id

  return config

