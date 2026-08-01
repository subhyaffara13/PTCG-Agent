
def checkpointables_metadata(
    path: path_types.PathLike,
) -> CheckpointMetadata[dict[str, AbstractCheckpointable]]:
  """Loads all checkpointables metadata from a checkpoint.

  This function is a more general version of `pytree_metadata`. The same
  `CheckpointMetadata` object is returned (with properties like
  `init_timestamp_nsecs` as shown above), but the type of the core `metadata`
  property is a dictionary, mapping checkpointable names to their metadata. This
  mirrors the return value of `load_checkpointables`, which similarly returns a
  dictionary mapping checkpointable names to their loaded values.

  For example::

    ocp.save_checkpointables(path, {
        'foo': Foo(),
        'bar': Bar(),
    })
    metadata = ocp.checkpointables_metadata(path)
    metadata.metadata  # {'foo': AbstractFoo(), 'bar': AbstractBar()}

  Args:
    path: The path to the checkpoint.

  Returns:
    A `CheckpointMetadata[dict[str, Any]]` object.
  """
  ctx = context_lib.get_context()
  path = ctx.file_options.path_class(path)
  layout = asyncio_utils.run_sync(
      layout_registry.get_checkpoint_layout(path, ctx.checkpoint_layout)
  )
  return _checkpointables_metadata_impl(layout, path)

