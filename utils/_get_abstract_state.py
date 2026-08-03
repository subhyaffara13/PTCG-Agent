from typing import Any

def _get_abstract_state(
    config: configs.CheckpointConfig,
    *,
    use_ocdbt: bool,
    devices: list[jax.Device] | None = None,
) -> Any:
  """Creates abstract state for a provided CheckpointConfig."""
  path = epath.Path(config.path)
  devices = devices or jax.devices()
  with checkpointer.Checkpointer(
      pytree_checkpoint_handler.PyTreeCheckpointHandler(use_ocdbt=use_ocdbt)
  ) as ckptr:
    metadata = ckptr.metadata(path).item_metadata

  if config.sharding_config_path is None:
    return get_abstract_state_with_generated_shardings(metadata.tree)
  return get_abstract_state_from_sharding_config(
      epath.Path(config.sharding_config_path), metadata, devices=devices
  )

