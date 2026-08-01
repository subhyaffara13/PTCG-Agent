
def _create_v0_savearg(
    param: ArraySerializationParam,
    context: context_lib.Context,
) -> type_handlers_v0.SaveArgs:
  """Creates a V0 `SaveArgs` from V1 params and context for saving."""
  storage_options = options_resolution.resolve_storage_options(
      param.keypath, param.value, context.array_options.saving
  )
  return type_handlers_v0.SaveArgs(
      dtype=jnp.dtype(storage_options.dtype) if storage_options.dtype else None,
      chunk_byte_size=storage_options.chunk_byte_size,
      shard_axes=storage_options.shard_axes,
  )


def _create_v0_savearg(
    param: NumpySerializationParam,
    context: context_lib.Context,
) -> type_handlers_v0.SaveArgs:
  """Creates a V0 `SaveArgs` from V1 params and context for saving."""
  storage_options = options_resolution.resolve_storage_options(
      param.keypath, param.value, context.array_options.saving
  )
  return type_handlers_v0.SaveArgs(
      dtype=np.dtype(storage_options.dtype) if storage_options.dtype else None,
      chunk_byte_size=storage_options.chunk_byte_size,
      shard_axes=storage_options.shard_axes,
  )


def _create_v0_savearg(
    param: ScalarSerializationParam,
    context: context_lib.Context,
) -> type_handlers_v0.SaveArgs:
  """Creates a V0 SaveArgs from V1 params and context for saving."""
  storage_options = options_resolution.resolve_storage_options(
      param.keypath, param.value, context.array_options.saving
  )
  return type_handlers_v0.SaveArgs(
      dtype=np.dtype(storage_options.dtype) if storage_options.dtype else None,
      chunk_byte_size=storage_options.chunk_byte_size,
      shard_axes=storage_options.shard_axes,
  )

