
def _slogdet_2x2(a: Array) -> tuple[Array, Array]:
  """Analytic slogdet for 2x2 matrices. No LU/solve."""
  a00, a01 = a[..., 0, 0], a[..., 0, 1]
  a10, a11 = a[..., 1, 0], a[..., 1, 1]
  det = (a00 * a11) - (a01 * a10)
  abs_det = ufuncs.abs(det)
  return ufuncs.sign(det), ufuncs.real(ufuncs.log(abs_det))

