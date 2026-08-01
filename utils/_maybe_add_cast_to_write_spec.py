
def _maybe_add_cast_to_write_spec(
    array_tspec: JsonSpec,
    *,
    dtype: DType,
    target_dtype: DType,
) -> JsonSpec:
  """Adds cast driver to a write array TensorStore spec, if needed."""
  if target_dtype == dtype:
    array_tspec['dtype'] = jnp.dtype(dtype).name
    return array_tspec

  array_tspec = {
      'base': array_tspec,
      'driver': 'cast',
  }
  # Origin dtype.
  array_tspec['dtype'] = jnp.dtype(dtype).name
  # Destination dtype.
  array_tspec['base']['dtype'] = jnp.dtype(target_dtype).name
  return array_tspec

