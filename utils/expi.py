
def expi(x: ArrayLike) -> Array:
  r"""Exponential integral function.

  JAX implementation of :obj:`scipy.special.expi`

  .. math::

     \mathrm{expi}(x) = \int_{-\infty}^x \frac{e^t}{t} \mathrm{d}t

  Args:
    x: arraylike, real-valued

  Returns:
    array of expi values

  See also:
    - :func:`jax.scipy.special.expn`
    - :func:`jax.scipy.special.exp1`
  """
  x_arr, = promote_args_inexact("expi", x)
  if dtypes.issubdtype(x_arr.dtype, np.complexfloating):
    raise ValueError("expi does not support complex-valued inputs.")
  return jnp.piecewise(x_arr, [x_arr < 0], [_expi_neg, _expi_pos])

