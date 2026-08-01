
def _as_bf16(x):
  return _ir_cast(x, _dtype_to_ir_type(jnp.bfloat16), signed=False)

