
def _convert_semaphore_type_to_aval(
    out_shape: SemaphoreType,
) -> jax_core.AbstractValue:
  return out_shape.get_array_aval()

