
def _get_v0_save_args(
    checkpointable: PyTree,
    array_saving_options: options_lib.ArrayOptions.Saving,
) -> PyTree:
  """Returns save args that are compatible with the V0 API."""
  def _leaf_get_v0_save_args(k, v):
    resolved_options = options_resolution.resolve_storage_options(
        k, v, array_saving_options
    )
    return type_handlers_v0.SaveArgs(
        dtype=np.dtype(resolved_options.dtype)
        if resolved_options.dtype is not None
        else None,
        chunk_byte_size=resolved_options.chunk_byte_size,
        shard_axes=resolved_options.shard_axes,
    )

  return jax.tree.map_with_path(_leaf_get_v0_save_args, checkpointable)

