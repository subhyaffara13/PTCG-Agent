from typing import Any

def _wrap_prng_keys(
    results: Sequence[Any],
    prng_info: dict[int, str],
) -> list[Any]:
  """Wraps physical output arrays back into PRNG key arrays."""
  result = list(results)
  if not prng_info:
    return result
  for i, impl in prng_info.items():
    if not is_prng_key_dtype(result[i].dtype):
      result[i] = jax.random.wrap_key_data(result[i], impl=impl)
  return result

