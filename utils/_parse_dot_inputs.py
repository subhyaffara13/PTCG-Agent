
def _parse_dot_inputs(*args, **kwargs):
  assert len(args) == 3
  x = args[0]
  k = args[1]
  dimension_numbers = args[2]

  # Use the `k.dtype` since it aligns with the `dtype` of its layers,
  # namely, the computation data type.
  comp_dtype = k.dtype
  x = jnp.asarray(x, comp_dtype)
  return x, k, dimension_numbers, comp_dtype

