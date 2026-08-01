
def _thin_qr_jvp(q, r, dx):
  """JVP for QR decompositions of [..., m, n] matrices with m >= n."""
  # See j-towns.github.io/papers/qr-derivative.pdf for a terse derivation.
  dx_rinv = triangular_solve(r, dx)  # Right side solve by default
  qt_dx_rinv = _H(q) @ dx_rinv
  qt_dx_rinv_lower = _tril(qt_dx_rinv, -1)
  do = qt_dx_rinv_lower - _H(qt_dx_rinv_lower)  # This is skew-symmetric

  # The following correction is necessary for complex inputs
  n = r.shape[-1]
  I = lax.expand_dims(lax._eye(do.dtype, (n, n)), range(qt_dx_rinv.ndim - 2))
  do = do + I * (qt_dx_rinv - qt_dx_rinv.real.astype(qt_dx_rinv.dtype))

  dq = q @ (do - qt_dx_rinv) + dx_rinv
  dr = (qt_dx_rinv - do) @ r
  return dq, dr

