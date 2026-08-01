
def gammasgn(x: ArrayLike) -> Array:
  r"""Sign of the gamma function.

  JAX implementation of :obj:`scipy.special.gammasgn`.

  .. math::

    \mathrm{gammasgn}(x) = \begin{cases}
      +1 & \Gamma(x) > 0 \\
      -1 & \Gamma(x) < 0
    \end{cases}

  Where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function.
  Because :math:`\Gamma(x)` is never zero, no condition is required for this case.

  * if :math:`x = -\infty`, NaN is returned.
  * if :math:`x = \pm 0`, :math:`\pm 1` is returned.
  * if :math:`x` is a negative integer, NaN is returned. The sign of gamma
    at a negative integer depends on from which side the pole is approached.
  * if :math:`x = \infty`, :math:`1` is returned.
  * if :math:`x` is NaN, NaN is returned.

  Args:
    x: arraylike, real valued.

  Returns:
    array containing the sign of the gamma function

  See Also:
    - :func:`jax.scipy.special.gamma`: the gamma function
    - :func:`jax.scipy.special.gammaln`: the natural log of the gamma function
  """
  x, = promote_args_inexact("gammasgn", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError("gammasgn does not support complex-valued inputs.")
  typ = x.dtype.type
  floor_x = lax.floor(x)
  x_negative = x < 0
  return jnp.select(
    [(x_negative & (x == floor_x)) | jnp.isnan(x),
     (x_negative & (floor_x % 2 != 0)) | ((x == 0) & jnp.signbit(x))],
    [typ(np.nan), typ(-1.0)],
    typ(1.0))

