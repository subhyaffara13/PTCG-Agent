
def exp1(x: ArrayLike) -> Array:
  r"""Exponential integral function.

  JAX implementation of :obj:`scipy.special.exp1`

  .. math::

     \mathrm{exp1}(x) = E_1(x) = x^{n-1}\int_x^\infty\frac{e^{-t}}{t}\mathrm{d}t


  Args:
    x: arraylike, real-valued

  Returns:
    array of exp1 values

  See also:
    - :func:`jax.scipy.special.expi`
    - :func:`jax.scipy.special.expn`
  """
  x, = promote_args_inexact("exp1", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError("exp1 does not support complex-valued inputs.")
  return expn(1, x)

