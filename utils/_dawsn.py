
def _dawsn(x: Array) -> Array:
  if x.dtype in [np.float32, np.float64]:
    return _dawsn_impl(x)
  else:  # float16, bfloat16 — upcast to float32
    return _dawsn_impl(x.astype(np.float32)).astype(x.dtype)

