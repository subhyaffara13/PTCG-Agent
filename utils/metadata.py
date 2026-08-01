
def metadata(distribution_name: str) -> _meta.PackageMetadata | None:
    """Get the metadata for the named package.

    :param distribution_name: The name of the distribution package to query.
    :return: A PackageMetadata containing the parsed metadata.
    """
    return Distribution.from_name(distribution_name).metadata


def metadata(distribution_name: str) -> _meta.PackageMetadata | None:
    """Get the metadata for the named package.

    :param distribution_name: The name of the distribution package to query.
    :return: A PackageMetadata containing the parsed metadata.
    """
    return Distribution.from_name(distribution_name).metadata


def metadata(
    path: path_types.PathLike,
    checkpointable_name: str | None = checkpoint_layout.AUTO_CHECKPOINTABLE_KEY,
) -> CheckpointMetadata[PyTreeMetadata]:
  """Loads the PyTree metadata from a checkpoint.

  This function retrieves metadata for a PyTree checkpoint, returning an
  object of type `CheckpointMetadata[PyTreeMetadata]`. Please see documentation
  on this class for further details.

  In short, the returned object contains a `metadata` attribute (among other
  attributes like timestamps), which is an instance of `PyTreeMetadata`. The
  `PyTreeMetadata` describes information specific to the PyTree itself. The most
  important such property is the PyTree structure, which is a tree structure
  matching the structure of the checkpointed PyTree, with leaf metadata objects
  describing each leaf.

  For example::

    metadata = ocp.metadata(path)  # CheckpointMetadata[PyTreeMetadata]
    metadata.metadata # PyTreeMetadata
    metadata.init_timestamp_nsecs  # Checkpoint creation timestamp.

    metadata.metadata  # PyTree structure.

  The metadata can then be used to inform checkpoint loading. For example::

    metadata = ocp.metadata(path)
    restored = ocp.load(path, metadata)

    # Load with altered properties.
    def _get_abstract_array(arr):
      # Assumes all checkpoint leaves are array types.
      new_dtype = ...
      new_sharding = ...
      return jax.ShapeDtypeStruct(arr.shape, new_dtype, sharding=new_sharding)

    metadata = dataclasses.replace(metadata,
          metadata=jax.tree.map(_get_abstract_array, metadata.metadata)
    )
    ocp.load(path, metadata)

  Args:
    path: The path to the checkpoint.
    checkpointable_name: The name of the checkpointable to load. A subdirectory
      with this name must exist in `path`. If None, then path itself is expected
      to contain all files relevant for loading the PyTree, rather than any
      subdirectory. Such files include, for example, `manifest.ocdbt`,
      `_METADATA`, `ocp.process_X`. Defaults to `AUTO`. Setting to `AUTO` mode
      dynamically discovers and resolves a pytree checkpointable. It prioritizes
      the standard 'pytree' checkpointable name if present, then sorts any other
      valid pytree checkpointable names alphabetically and returns the first
      valid one, and ultimately falls back to interpreting the path as a flat V0
      root layout if no standard pytree exists.

  Returns:
    A `CheckpointMetadata[PyTreeMetadata]` object.
  """
  validation.validate_state_checkpointable_name(checkpointable_name)
  ctx = context_lib.get_context()
  path = ctx.file_options.path_class(path)

  resolver = asyncio_utils.run_sync(
      layout_registry.CheckpointLayoutResolver.resolve(
          path, ctx.checkpoint_layout, pytree_name=checkpointable_name
      )
  )
  layout = resolver.layout
  resolved_name = resolver.pytree_name

  async def _load_metadata() -> CheckpointMetadata[PyTreeMetadata]:
    return await layout.metadata(path, resolved_name)

  state_metadata = asyncio_utils.run_sync(_load_metadata())
  validation.validate_abstract_state(state_metadata.metadata)
  return CheckpointMetadata[PyTreeMetadata](
      path=path,
      metadata=state_metadata.metadata,
      init_timestamp_nsecs=state_metadata.init_timestamp_nsecs,
      commit_timestamp_nsecs=state_metadata.commit_timestamp_nsecs,
      custom_metadata=state_metadata.custom_metadata,
  )

