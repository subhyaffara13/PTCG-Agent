
def _construct_serialization_context(
    info: types_v0.ParamInfo,
) -> types.SerializationContext:
  return types.SerializationContext(
      # TODO(dnlng): should use actual wait
      parent_dir=_PathAwaitingCreation(
          info.parent_dir, synchronization.get_operation_id()
      ),
      ts_context=info.ts_context,
      byte_limiter=info.byte_limiter,
      device_host_byte_limiter=info.device_host_byte_limiter,
  )

