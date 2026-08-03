from typing import Any

def _get_underlying_shape(
    shape: tuple[int, ...] | None, dtype: Any
) -> tuple[int, ...] | None:
  """Returns the data shape for underlying data of PRNG keys."""
  if shape is None:
    return None
  return jax.eval_shape(
      jax.random.key_data, jax.ShapeDtypeStruct(shape=shape, dtype=dtype)
  ).shape

