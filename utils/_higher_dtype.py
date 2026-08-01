
def _higher_dtype(
    dtype1: jax.typing.DTypeLike, dtype2: jax.typing.DTypeLike
) -> jax.typing.DTypeLike:
  """Returns higher dtype among two dtypes, if any can be promoted to the other.

  Args:
    dtype1: The first dtype to compare.
    dtype2: The second dtype to compare.

  Returns:
    The highest of the two dtypes, if any can be promoted to the other.

  Raises:
    ValueError: If none of the dtypes can be promoted to the other.
  """
  if _lower_dtype(dtype1, dtype2) == dtype1:
    return dtype2
  else:
    return dtype1

