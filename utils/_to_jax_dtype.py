
def _to_jax_dtype(tf_dtype):
  # Note that converting _to_tf_dtype and _to_jax_dtype are not inverses,
  # due to float0 and 64-bit behavior.
  dt = dtypes.canonicalize_dtype(tf_dtype.as_numpy_dtype)
  if dt not in dtypes._jax_dtype_set:
    raise TypeError(f"dtype {dt} is not a valid JAX array "
                    "type. Only arrays of numeric types are supported by JAX.")
  return dt

