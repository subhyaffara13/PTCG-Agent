
def _unwrap_prng_keys(
    args_leaves: Sequence[Any],
    prng_info: dict[int, str],
) -> list[Any]:
  """Converts PRNG key arrays to their physical representation."""
  result = list(args_leaves)
  if not prng_info:
    return result
  for i in prng_info:
    if is_prng_key_dtype(result[i].dtype):
      result[i] = jax.random.key_data(result[i])
  return result

