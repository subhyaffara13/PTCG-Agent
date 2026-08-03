from typing import Any

def _create_checkpoint_manager(
    local_directory: epath.Path,
    persistent_directory: epath.Path,
    global_mesh: jax.sharding.Mesh,
    abstract_state: Any,
    options: EcmBenchmarkOptions,
) -> emergency_checkpoint_manager.CheckpointManager:
  """Creates an EmergencyCheckpointManager."""
  return emergency_checkpoint_manager.CheckpointManager(
      local_directory=local_directory,
      persistent_directory=persistent_directory,
      global_mesh=global_mesh,
      abstract_state=abstract_state,
      options=emergency_checkpoint_manager.CheckpointManagerOptions(
          local=emergency_checkpoint_manager.LocalCheckpointOptions(
              save_interval_steps=options.local_save_interval_steps,
              max_to_keep=options.local_max_to_keep,
          ),
          persistent=emergency_checkpoint_manager.PersistentCheckpointOptions(
              save_interval_steps=options.persistent_save_interval_steps,
              max_to_keep=options.persistent_max_to_keep,
          ),
          replica_axis_index=options.replica_axis_index,
          single_host_load_and_broadcast=options.single_host_load_and_broadcast,
      ),
  )


def _create_checkpoint_manager(
    local_directory: epath.Path,
    persistent_directory: epath.Path,
    global_mesh: jax.sharding.Mesh,
    abstract_state: Any,
    options: P2pBenchmarkOptions,
) -> p2p_checkpoint_manager.CheckpointManager:
  """Creates a P2P CheckpointManager."""
  return p2p_checkpoint_manager.CheckpointManager(
      local_directory=local_directory,
      persistent_directory=persistent_directory,
      global_mesh=global_mesh,
      abstract_state=abstract_state,
      options=p2p_options.CheckpointManagerOptions(
          local=p2p_options.LocalCheckpointOptions(
              save_interval_steps=options.local_save_interval_steps,
              max_to_keep=options.local_max_to_keep,
          ),
          persistent=p2p_options.PersistentCheckpointOptions(
              save_interval_steps=options.persistent_save_interval_steps,
              max_to_keep=options.persistent_max_to_keep,
          ),
          replica_axis_index=options.replica_axis_index,
      ),
  )

