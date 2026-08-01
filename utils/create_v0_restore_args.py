
def create_v0_restore_args(
    context: context_lib.Context,
    abstract_checkpointable: PyTree | None,
) -> base_pytree_checkpoint_handler.BasePyTreeRestoreArgs:
  """Creates v0 CheckpointArgs for restoration."""

  if abstract_checkpointable is not None:
    restore_args = jax.tree.map(
        lambda checkpointable: compatibility.V0RestoreArgs(
            restore_type=_restore_type_by_abstract_type(checkpointable),
            abstract_leaf=checkpointable,
        ),
        abstract_checkpointable,
    )
  else:
    restore_args = None

  logging.vlog(1, 'restore_args: %s', restore_args)

  return base_pytree_checkpoint_handler.BasePyTreeRestoreArgs(
      item=abstract_checkpointable,
      restore_args=restore_args,
      partial_restore=context.pytree_options.loading.partial_load,
  )

