
def _erfcx(x: Array) -> Array:
  if x.dtype == np.float64:
    # At threshold ~26.6, first omitted term |c_9|/x^18 ~ 1e-21 << eps64 ~ 2e-16.
    return _erfcx_impl(x, nterms=9)
  elif x.dtype == np.float32:
    # At threshold ~9.4, first omitted term |c_5|/x^10 ~ 5e-9 << eps32 ~ 1e-7.
    return _erfcx_impl(x, nterms=5)
  else:  # float16, bfloat16 — upcast to float32
    return _erfcx_impl(x.astype(np.float32), nterms=5).astype(x.dtype)

