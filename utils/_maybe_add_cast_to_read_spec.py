
def _maybe_add_cast_to_read_spec(
    array_tspec: JsonSpec,
    *,
    dtype: DType,
) -> JsonSpec:
  """Adds cast driver to a read array TensorStore spec, if needed."""
  if not jax.dtypes.issubdtype(
      dtype, jax.dtypes.prng_key
  ):
    array_tspec = {
        'base': array_tspec,
        'driver': 'cast',
        'dtype': jnp.dtype(dtype).name,
    }
  return array_tspec

