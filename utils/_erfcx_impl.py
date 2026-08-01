
def _erfcx_impl(x: Array, nterms: int) -> Array:
  # Switch to asymptotic expansion when exp(x^2) would overflow.
  # Overflow occurs when x^2 > log(fmax), i.e. x > sqrt(log(fmax)).
  threshold = np.sqrt(np.log(dtypes.finfo(x.dtype).max))
  large = x > _lax_const(x, threshold)
  safe_x = lax.select(large, lax.full_like(x, 1.), x)
  direct = lax.exp(lax.square(safe_x)) * lax.erfc(safe_x)
  asymp = _erfcx_asymptotic(x, nterms)
  return lax.select(large, asymp, direct)

