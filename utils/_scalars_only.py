
def _scalars_only(
  path: tuple[Key, ...], scalar_key: jax.Array, target_shape: tuple[int, ...]
) -> jax.Array:
  if target_shape != ():
    raise ValueError(
      f'Cannot reseed stream at path {path!r} becuase it has a non-scalar key, '
      f'found key with shape {target_shape}. If all your multi-dimensional '
      'keys have unique values on all dimensions, set policy="match_shape", '
      'else provide a custom reseed policy.'
    )
  return scalar_key

