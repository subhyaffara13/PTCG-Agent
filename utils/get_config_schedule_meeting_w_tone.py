
def get_config_schedule_meeting_w_tone(
    config: ml_collections.config_dict.ConfigDict,
):
  """Get config for imitation dataset construction of meeting scheduling dow."""

  config.config_rnd = config_schedule_meeting_w_tone.get_config()
  config.new_config = same_scenario_config

  return config

