
def _to_tf_dtype(jax_dtype):
  # Note that converting _to_tf_dtype and _to_jax_dtype are not inverses,
  # due to float0 and 64-bit behavior.
  try:
    jax_dtype = _jax_physical_dtype(jax_dtype)
  except TypeError:
    # `jax_dtype` isn't actually a valid jax dtype (e.g. it is
    # tf.float32), so there is no physical dtype anyway
    pass
  if jax_dtype == dtypes.float0:
    jax_dtype = _tf_np_dtype_for_float0
  return tf.dtypes.as_dtype(jax_dtype)

