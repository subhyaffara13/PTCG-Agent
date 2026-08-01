
def _trace_value_abstract_eval(value, *, label):
  del label
  if value.shape:
    raise ValueError(
        f"trace_value requires a scalar value, got shape {value.shape}"
    )
  if value.dtype not in (jnp.int32, jnp.float32):
    raise ValueError(f"trace_value requires i32 or f32, got {value.dtype}")
  return [], {trace_effect}

