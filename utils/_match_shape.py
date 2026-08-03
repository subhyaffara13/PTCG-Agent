import random

def _match_shape(
  path: tuple[Key, ...], scalar_key: jax.Array, target_shape: tuple[int, ...]
) -> jax.Array:
  if target_shape == ():
    return scalar_key
  return random.split(scalar_key, target_shape)

