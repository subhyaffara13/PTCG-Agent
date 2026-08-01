
def i0e(a: TensorLikeType) -> TensorLikeType:
    return prims.bessel_i0e(a)


def i0e(x: ArrayLike) -> Array:
  r"""Exponentially scaled modified bessel function of zeroth order.

  JAX implementation of :obj:`scipy.special.i0e`.

  .. math::

     \mathrm{i0e}(x) = e^{-|x|} I_0(x)

  where :math:`I_0(x)` is the modified Bessel function :func:`~jax.scipy.special.i0`.

  Args:
    x: array, real-valued

  Returns:
    array of bessel function values.

  See also:
    - :func:`jax.scipy.special.i0`
    - :func:`jax.scipy.special.i1`
    - :func:`jax.scipy.special.i1e`
  """
  x, = promote_args_inexact("i0e", x)
  return lax.bessel_i0e(x)

