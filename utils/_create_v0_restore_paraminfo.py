
def _create_v0_restore_paraminfo(
    param: (
        types.DeserializationParam[None]
        | types.DeserializationParam[AbstractShardedArray]
    ),
    context: context_lib.Context,
    deserialization_context: types.DeserializationContext,
) -> type_handlers_v0.ParamInfo:
  """Creates a V0 `ParamInfo` from V1 params and contexts for loading."""

  loading_options = context.array_options.loading

  if isinstance(param.value, ArrayMetadata):
    # the write_shape is populated for metadata() calls.
    v = cast(ArrayMetadata, param.value)
    if v.storage_metadata is not None:
      write_shape = v.storage_metadata.write_shape
    else:
      write_shape = None
  else:
    write_shape = None

  return type_handlers_v0.ParamInfo(
      name=param.name,
      parent_dir=deserialization_context.parent_dir,
      skip_deserialize=False,
      byte_limiter=deserialization_context.byte_limiter,
      is_ocdbt_checkpoint=deserialization_context.ocdbt_checkpoint,
      ts_context=deserialization_context.ts_context,
      raise_array_data_missing_error=loading_options.raise_array_data_missing_error,
      use_zarr3=deserialization_context.zarr3_checkpoint,
      write_shape=write_shape,
  )


def _create_v0_restore_paraminfo(
    param: types.DeserializationParam[AbstractArray | None],
    context: context_lib.Context,
    deserialization_context: types.DeserializationContext,
) -> type_handlers_v0.ParamInfo:
  """Creates a V0 `ParamInfo` from V1 params and contexts for loading."""

  loading_options = context.array_options.loading

  return type_handlers_v0.ParamInfo(
      name=param.name,
      parent_dir=deserialization_context.parent_dir,
      skip_deserialize=False,
      byte_limiter=deserialization_context.byte_limiter,
      is_ocdbt_checkpoint=deserialization_context.ocdbt_checkpoint,
      ts_context=deserialization_context.ts_context,
      raise_array_data_missing_error=loading_options.raise_array_data_missing_error,
      use_zarr3=deserialization_context.zarr3_checkpoint,
  )


def _create_v0_restore_paraminfo(
    param: types.DeserializationParam[
        AbstractScalar | Type[AbstractScalar] | None
    ],
    context: context_lib.Context,
    deserialization_context: types.DeserializationContext,
) -> type_handlers_v0.ParamInfo:
  """Creates a V0 ParamInfo from V1 params and contexts for loading."""

  loading_options = context.array_options.loading

  return type_handlers_v0.ParamInfo(
      name=param.name,
      parent_dir=deserialization_context.parent_dir,
      skip_deserialize=False,
      byte_limiter=deserialization_context.byte_limiter,
      is_ocdbt_checkpoint=deserialization_context.ocdbt_checkpoint,
      ts_context=deserialization_context.ts_context,
      raise_array_data_missing_error=loading_options.raise_array_data_missing_error,
      use_zarr3=deserialization_context.zarr3_checkpoint,
  )

