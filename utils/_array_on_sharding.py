
def _array_on_sharding(
    value: np.ndarray,
    sharding: jax.sharding.Sharding,
) -> jax.Array:
  """Creates a JAX array with the given value on the specified sharding.

  Args:
    value: The numpy array containing the data.
    sharding: The sharding to use for the JAX array.

  Returns:
    A JAX array with the same shape and dtype as `value`, sharded according to
    `sharding`.
  """

  def data_callback(index):
    if index is None:
      return value
    return value[index]

  return jax.make_array_from_callback(
      value.shape,
      sharding,
      data_callback,
      dtype=value.dtype,
  )

