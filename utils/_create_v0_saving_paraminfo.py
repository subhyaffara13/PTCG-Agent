
def _create_v0_saving_paraminfo(
    param: ArraySerializationParam,
    context: context_lib.Context,
    serialization_context: types.SerializationContext,
) -> type_handlers_v0.ParamInfo:
  """Creates a V0 `ParamInfo` from V1 params and contexts for saving."""

  saving_options = context.array_options.saving

  return type_handlers_v0.ParamInfo(
      name=param.name,
      parent_dir=serialization_context.parent_dir.path,
      byte_limiter=serialization_context.byte_limiter,
      device_host_byte_limiter=serialization_context.device_host_byte_limiter,
      is_ocdbt_checkpoint=saving_options.use_ocdbt,
      use_zarr3=saving_options.use_zarr3,
      use_compression=saving_options.use_compression,
      ocdbt_target_data_file_size=saving_options.ocdbt_target_data_file_size,
      ts_context=serialization_context.ts_context,
      value_typestr=None,  # TODO(dnlng): Add value typestr.
      enable_pinned_host_transfer=saving_options.enable_pinned_host_transfer,
  )


def _create_v0_saving_paraminfo(
    param: NumpySerializationParam,
    context: context_lib.Context,
    serialization_context: types.SerializationContext,
) -> type_handlers_v0.ParamInfo:
  """Creates a V0 `ParamInfo` from V1 params and contexts for saving."""

  saving_options = context.array_options.saving

  return type_handlers_v0.ParamInfo(
      name=param.name,
      parent_dir=serialization_context.parent_dir.path,
      byte_limiter=serialization_context.byte_limiter,
      device_host_byte_limiter=serialization_context.device_host_byte_limiter,
      is_ocdbt_checkpoint=saving_options.use_ocdbt,
      use_zarr3=saving_options.use_zarr3,
      use_compression=saving_options.use_compression,
      ocdbt_target_data_file_size=saving_options.ocdbt_target_data_file_size,
      ts_context=serialization_context.ts_context,
      value_typestr='np.ndarray',
  )


def _create_v0_saving_paraminfo(
    param: ScalarSerializationParam,
    context: context_lib.Context,
    serialization_context: types.SerializationContext,
) -> type_handlers_v0.ParamInfo:
  """Creates a V0 ParamInfo from V1 params andn contexts for saving."""

  saving_options = context.array_options.saving

  return type_handlers_v0.ParamInfo(
      name=param.name,
      parent_dir=serialization_context.parent_dir.path,
      byte_limiter=serialization_context.byte_limiter,
      device_host_byte_limiter=serialization_context.device_host_byte_limiter,
      is_ocdbt_checkpoint=saving_options.use_ocdbt,
      use_zarr3=saving_options.use_zarr3,
      use_compression=saving_options.use_compression,
      ocdbt_target_data_file_size=saving_options.ocdbt_target_data_file_size,
      ts_context=serialization_context.ts_context,
      value_typestr="scalar",
  )

