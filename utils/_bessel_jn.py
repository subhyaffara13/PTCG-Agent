
def _bessel_jn(z: ArrayLike, *, v: int, n_iter: int=50) -> Array:
  f0 = _lax_const(z, 0.0)
  f1 = _lax_const(z, 1E-16)
  f = _lax_const(z, 0.0)
  bs = _lax_const(z, 0.0)

  (_, _, bs, _), j_vals = lax.scan(
      f=_bessel_jn_scan_body_fun, init=(f0, f1, bs, z),
      xs=lax.iota(lax.dtype(z), n_iter+1), reverse=True)

  f = j_vals[0]  # Use the value at the last iteration.
  j_vals = j_vals[:v+1]
  j_vals = j_vals / (bs - f)

  return j_vals

