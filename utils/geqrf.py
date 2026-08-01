
def geqrf(a: ArrayLike) -> tuple[Array, Array]:
  """Computes the QR decomposition of a matrix.

  Args:
    a: an ``[..., m, n]`` batch of matrices, with floating-point or complex type.
  Returns:
    An ``(a, taus)`` pair where ``r`` is in the upper triangle of ``a``,
    ``q`` is represented in the lower triangle of ``a`` and in ``taus`` as
    elementary Householder reflectors.
  """
  a_out, taus = geqrf_p.bind(a)
  return a_out, taus

