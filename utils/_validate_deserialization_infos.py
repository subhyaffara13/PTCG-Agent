
def _validate_deserialization_infos(
    infos: Sequence[types_v0.ParamInfo],
) -> None:
  """Validates that all infos share the same properties."""
  info0 = infos[0]
  for info in infos:
    if (
        info0.parent_dir != info.parent_dir
        or info0.is_ocdbt_checkpoint != info.is_ocdbt_checkpoint
        or info0.use_zarr3 != info.use_zarr3
        or info0.ts_context != info.ts_context
        or info0.byte_limiter != info.byte_limiter
    ):
      raise ValueError(
          'All infos must have the same parent_dir, is_ocdbt_checkpoint,'
          ' use_zarr3, ts_context, and byte_limiter.'
      )

