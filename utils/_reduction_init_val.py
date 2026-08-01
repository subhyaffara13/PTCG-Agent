
def _reduction_init_val(a: Array, init_val: Any) -> np.ndarray:
  # This function uses np.* functions because lax pattern matches against the
  # specific concrete values of the reduction inputs.
  a_dtype = a.dtype
  if a_dtype == 'bool':
    return np.array(init_val > 0, dtype=a_dtype)
  if (np.isinf(init_val) and dtypes.issubdtype(a_dtype, np.floating)
      and not dtypes.supports_inf(a_dtype)):
    init_val = np.array(dtypes.finfo(a_dtype).min if np.isneginf(init_val)
                        else dtypes.finfo(a_dtype).max, dtype=a_dtype)
  try:
    return np.array(init_val, dtype=a_dtype)
  except OverflowError:
    assert dtypes.issubdtype(a_dtype, np.integer)
    sign, info = np.sign(init_val), dtypes.iinfo(a_dtype)
    return np.array(info.min if sign < 0 else info.max, dtype=a_dtype)

