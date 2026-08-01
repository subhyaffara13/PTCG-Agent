
def create_checkpoint_manager(
    global_mesh: jax.sharding.Mesh,
    abstract_state: PyTree,
    local_directory: epath.Path,
    persistent_directory: epath.Path,
    *,
    use_async: bool = True,
    replica_axis_index: int = 0,
) -> CheckpointManager:
  """Create CheckpointManager for testing."""
  options = CheckpointManagerOptions(
      local=LocalCheckpointOptions(save_interval_steps=2, max_to_keep=2),
      persistent=PersistentCheckpointOptions(
          save_interval_steps=5, max_to_keep=3
      ),
      enable_async_checkpointing=use_async,
      replica_axis_index=replica_axis_index,
  )
  return CheckpointManager(
      local_directory=local_directory,
      persistent_directory=persistent_directory,
      global_mesh=global_mesh,
      abstract_state=abstract_state,
      options=options,
  )

