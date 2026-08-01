
def bessel_i0e(x): return scipy.special.i0e(x).astype(x.dtype)


def bessel_i0e(x: ArrayLike) -> Array:
  r"""Exponentially scaled modified Bessel function of order 0:
  :math:`\mathrm{i0e}(x) = e^{-|x|} \mathrm{i0}(x)`
  """
  return bessel_i0e_p.bind(x)

