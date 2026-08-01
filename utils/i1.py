
def i1(a: TensorLikeType) -> TensorLikeType:
    return prims.bessel_i1(a)


def i1(x: ArrayLike) -> Array:
  r"""Modified bessel function of first order.

  JAX implementation of :obj:`scipy.special.i1`.

  .. math::

     \mathrm{i1}(x) = I_1(x) = \frac{1}{2}x\sum_{k=0}^\infty\frac{(x^2/4)^k}{k!(k+1)!}

  Args:
    x: array, real-valued

  Returns:
    array of bessel function values

  See also:
    - :func:`jax.scipy.special.i0`
    - :func:`jax.scipy.special.i0e`
    - :func:`jax.scipy.special.i1e`
  """
  x, = promote_args_inexact("i1", x)
  return lax.mul(lax.exp(lax.abs(x)), lax.bessel_i1e(x))

