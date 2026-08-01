
def i1e(a: TensorLikeType) -> TensorLikeType:
    return prims.bessel_i1e(a)


def i1e(x: ArrayLike) -> Array:
  r"""Exponentially scaled modified bessel function of first order.

  JAX implementation of :obj:`scipy.special.i1e`.

  .. math::

     \mathrm{i1e}(x) = e^{-|x|} I_1(x)

  where :math:`I_1(x)` is the modified Bessel function :func:`~jax.scipy.special.i1`.

  Args:
    x: array, real-valued

  Returns:
    array of bessel function values

  See also:
    - :func:`jax.scipy.special.i0`
    - :func:`jax.scipy.special.i0e`
    - :func:`jax.scipy.special.i1`
  """
  x, = promote_args_inexact("i1e", x)
  return lax.bessel_i1e(x)

