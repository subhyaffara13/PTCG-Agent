
def _as_f32(x):
  return _ir_cast(x, _dtype_to_ir_type(jnp.float32), signed=False)

