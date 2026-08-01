
def load_checkpoint(config: configs.CheckpointConfig) -> Any:
  """Loads a PyTree of test checkpoint from a provided path.

  Constructs a checkpoint from a reference checkpoint path specified in the
  config, which is expected to be provided. The checkpoint will be sharded
  according to an opaque strategy intended to minimize memory footprint, or will
  use the sharding config specified in `config` if provided.

  Args:
      config: A CheckpointConfig object allowing the checkpoint to be loaded
        from a reference or generated from a spec.

  Returns:
      A PyTree containing the loaded checkpoint.
  """
  if config.path is None:
    raise ValueError(
        'CheckpointConfig must have a `path` if `spec` is not provided.'
    )
  logging.info('Loading checkpoint from path: %s', config.path)
  path = epath.Path(config.path)


  use_ocdbt = type_handlers.is_ocdbt_checkpoint(path)
  abstract_state = _get_abstract_state(config, use_ocdbt=use_ocdbt)
  restore_args = checkpoint_utils.construct_restore_args(abstract_state)

  if multihost.is_pathways_backend():
    checkpointing_impl = pathways.CheckpointingImpl.from_options(
        use_colocated_python=config.load_with_colocated_python,
    )
    pathways.register_type_handlers(
        checkpointing_impl=checkpointing_impl,
        use_replica_parallel=False,
        enable_replica_parallel_separate_folder=False,
    )

  with checkpointer.Checkpointer(
      pytree_checkpoint_handler.PyTreeCheckpointHandler(use_ocdbt=use_ocdbt)
  ) as ckptr:
    pytree = ckptr.restore(
        path,
        args=pytree_checkpoint_handler.PyTreeRestoreArgs(
            restore_args=restore_args
        ),
    )
  return tree_utils.serialize_tree(pytree, keep_empty_nodes=True)

