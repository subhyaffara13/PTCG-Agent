
def get_config_trade_fruit_w_tone(
    config: ml_collections.config_dict.ConfigDict,
):
  """Get config for imitation dataset construction of trading fruit."""

  config.config_rnd = config_trade_fruit_w_tone.get_config()
  config.new_config = same_scenario_config

  return config

