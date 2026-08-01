
def _slogdet_1x1(a: Array) -> tuple[Array, Array]:
  """Analytic slogdet for 1x1 matrices. No LU/solve"""
  det = a[..., 0, 0]
  abs_det = ufuncs.abs(det)
  return ufuncs.sign(det), ufuncs.real(ufuncs.log(abs_det))

