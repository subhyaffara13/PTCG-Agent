
def create_v0_save_args(
    context: context_lib.Context,
    checkpointable: PyTree,
) -> base_pytree_checkpoint_handler.BasePyTreeSaveArgs:
  """Creates v0 CheckpointArgs for saving."""
  return base_pytree_checkpoint_handler.BasePyTreeSaveArgs(
      item=checkpointable,
      save_args=_get_v0_save_args(
          checkpointable,
          context.array_options.saving,
      ),
      ocdbt_target_data_file_size=context.array_options.saving.ocdbt_target_data_file_size,
  )

