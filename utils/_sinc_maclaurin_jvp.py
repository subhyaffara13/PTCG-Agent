
def _sinc_maclaurin_jvp(k, primals, tangents):
  (x,), (t,) = primals, tangents
  return _sinc_maclaurin(k, x), _sinc_maclaurin(k + 1, x) * t

