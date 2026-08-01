
def create_game_with_setting(game_name: str,
                             setting: Optional[str] = None) -> pyspiel.Game:
  """Creates an OpenSpiel game with the specified setting.

  Args:
    game_name: Name of a registered game, e.g. mfg_crowd_modelling_2d.
    setting: Name of the pre-defined setting. If None, game_name will be used
      instead. The setting should be present in the GAME_SETTINGS map above.

  Returns:
    a Game.
  """
  setting = setting or game_name
  params = GAME_SETTINGS.get(setting)
  if params is None:
    raise ValueError(f"{setting} setting does not exist for {game_name}.")

  logging.info("Creating %s game with parameters: %r", game_name, params)

  # Dynamic routing game requires setting the network and demand explicitly.
  if game_name == "python_mfg_dynamic_routing":
    # Create a copy since we modify it below removing the network key.
    params = params.copy()
    network = params.pop("network")
    network, od_demand = DYNAMIC_ROUTING_NETWORK[network]
    return dynamic_routing.MeanFieldRoutingGame(
        params, network=network, od_demand=od_demand)

  return pyspiel.load_game(game_name, params)

