
def make_scalar_array_like(
    value: Any, like: jax.Array, *, dtype: Any
) -> jax.Array:
  """Builds a scalar array on the same global sharding as `like`.

  Using `jax.device_put(..., sharding=...)` on a non-fully-addressable global
  sharding can trigger multihost consistency checks. Constructing the result via
  callback avoids that path while preserving the target sharding.

  Args:
    value: The scalar value to fill the array with.
    like: An array whose sharding and shape will be copied.
    dtype: The desired dtype of the result.

  Returns:
    A new array with the same shape and sharding as `like`, filled with `value`.
  """
  return jax.make_array_from_callback(
      like.shape,
      like.sharding,
      lambda _: np.asarray(value, dtype=dtype),
      dtype=dtype,
  )

