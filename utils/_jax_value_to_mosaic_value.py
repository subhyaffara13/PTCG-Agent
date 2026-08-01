
def _jax_value_to_mosaic_value(x: jax.Array) -> jax.Array:
  if dtypes.issubdtype(x.dtype, dtypes.bool_):
    return x.astype(lowering.BOOL_MEMREF_TYPE)
  return x

