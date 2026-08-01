
def _lower_dtype(
    dtype1: jax.typing.DTypeLike, dtype2: jax.typing.DTypeLike
) -> jax.typing.DTypeLike:
  """Returns lower dtype among two dtypes, if any can be promoted to the other.

  Args:
    dtype1: The first dtype to compare.
    dtype2: The second dtype to compare.

  Returns:
    The lowest of the two dtypes, if any can be promoted to the other.

  Raises:
    ValueError: If none of the dtypes can be promoted to the other.
  """
  if jnp.promote_types(dtype1, dtype2) == dtype1:
    return dtype2
  if jnp.promote_types(dtype1, dtype2) == dtype2:
    return dtype1
  raise ValueError(
      f'Cannot compare dtype of {dtype1=} and {dtype2=}.'
      f' Neither {dtype1} nor {dtype2} can be promoted to the other.'
  )

