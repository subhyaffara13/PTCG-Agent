
def ndtri(a: TensorLikeType) -> TensorLikeType:
    return prims.ndtri(a)


def ndtri(p: ArrayLike) -> Array:
  r"""The inverse of the CDF of the Normal distribution function.

  JAX implementation of :obj:`scipy.special.ndtri`.

  Returns `x` such that the area under the PDF from :math:`-\infty` to `x` is equal
  to `p`.

  A piece-wise rational approximation is done for the function.
  This is based on the implementation in netlib.

  Args:
    p: an array of type `float32`, `float64`.

  Returns:
    an array with `dtype=p.dtype`.

  Raises:
    TypeError: if `p` is not floating-type.
  """
  dtype = lax.dtype(p)
  if dtype not in (np.float32, np.float64):
    raise TypeError(
        "x.dtype={} is not supported, see docstring for supported types."
        .format(dtype))
  return _ndtri(p)

