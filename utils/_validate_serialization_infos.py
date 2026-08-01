
def _validate_serialization_infos(
    infos: Sequence[types_v0.ParamInfo],
) -> None:
  """Validates that all infos share the same properties."""
  info0 = infos[0]
  for info in infos[1:]:
    if (
        (info0.parent_dir != info.parent_dir)
        or (info0.ts_context != info.ts_context)
        or (info0.byte_limiter != info.byte_limiter)
        or (info0.device_host_byte_limiter != info.device_host_byte_limiter)
    ):
      raise ValueError(
          'All infos must have the same parent_dir, ts_context, byte_limiter,'
          ' and device_host_byte_limiter.'
      )

