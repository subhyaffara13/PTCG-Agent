
def get_config_debate(config: ml_collections.config_dict.ConfigDict):
  """Get config for imitation dataset construction of debates."""

  config.config_rnd = config_debate.get_config()
  config.new_config = new_debate_scenario_config

  return config

