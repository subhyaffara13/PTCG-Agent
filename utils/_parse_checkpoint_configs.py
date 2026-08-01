
def _parse_checkpoint_configs(
    config: dict[str, Any],
) -> list[config_lib.CheckpointConfig]:
  """Builds the checkpoint configs from the YAML; defaults to a single one."""
  if 'checkpoint_configs' in config:
    return [
        config_lib.CheckpointConfig(**cc) for cc in config['checkpoint_configs']
    ]
  if 'checkpoint_config' in config:
    return [config_lib.CheckpointConfig(**config['checkpoint_config'])]
  return [config_lib.CheckpointConfig()]

