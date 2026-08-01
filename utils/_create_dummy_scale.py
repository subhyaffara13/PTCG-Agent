
def _create_dummy_scale(operand, contracting_dims):
  shape = list(operand.shape)
  for d in contracting_dims:
    shape[d] = 1
  return jnp.ones(shape, dtype=jnp.bfloat16).astype(dtypes.float8_e8m0fnu)

