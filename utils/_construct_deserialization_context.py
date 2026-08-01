
def _construct_deserialization_context(
    info: types_v0.ParamInfo,
) -> types.DeserializationContext:
  return types.DeserializationContext(
      parent_dir=info.parent_dir,
      ocdbt_checkpoint=info.is_ocdbt_checkpoint,
      zarr3_checkpoint=info.use_zarr3,
      ts_context=info.ts_context,
      byte_limiter=info.byte_limiter,
  )

