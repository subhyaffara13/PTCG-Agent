
def safe_increment(count: jax.typing.ArrayLike) -> jax.typing.ArrayLike:
  """Increments counter by one while avoiding overflow.

  Denote ``max_val``, ``min_val`` as the maximum, minimum, possible values for
  the ``dtype`` of ``count``. Normally ``max_val + 1`` would overflow to
  ``min_val``. This functions ensures that when ``max_val`` is reached the
  counter stays at ``max_val``.

  Args:
    count: a counter to be incremented.

  Returns:
    A counter incremented by 1, or ``max_val`` if the maximum value is
    reached.

  Examples:
    >>> import jax.numpy as jnp
    >>> import optax
    >>> optax.safe_increment(jnp.asarray(1, dtype=jnp.int32))
    Array(2, dtype=int32)
    >>> optax.safe_increment(jnp.asarray(2147483647, dtype=jnp.int32))
    Array(2147483647, dtype=int32)

  .. versionadded:: 0.2.4
  """
  count_dtype = jnp.asarray(count).dtype
  if jnp.issubdtype(count_dtype, jnp.integer):
    max_value = jnp.iinfo(count_dtype).max
  elif jnp.issubdtype(count_dtype, jnp.floating):
    max_value = jnp.finfo(count_dtype).max
  else:
    raise ValueError(
        f'Cannot safely increment count with dtype {count_dtype},'
        ' valid dtypes are subdtypes of "jnp.integer" or "jnp.floating".'
    )
  max_value = jnp.array(max_value, count_dtype)
  one = jnp.array(1, count_dtype)
  return jnp.where(count < max_value, count + one, max_value)

