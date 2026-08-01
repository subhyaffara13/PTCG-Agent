
def jnp_to_np_array(arr: pytypes.Array) -> np.ndarray:
  """Converts `jnp.ndarray` to `np.ndarray`."""
  if getattr(arr, "dtype", None) == jnp.bfloat16:
    # Numpy does not support `bfloat16`.
    arr = arr.astype(jnp.float32)
  return jax.device_get(arr)

