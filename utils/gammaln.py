
def gammaln(x: ArrayLike) -> Array:
  r"""Natural log of the absolute value of the gamma function.

  JAX implementation of :obj:`scipy.special.gammaln`.

  .. math::

     \mathrm{gammaln}(x) = \log(|\Gamma(x)|)

  Where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    x: arraylike, real valued.

  Returns:
    array containing the values of the log-gamma function

  See Also:
    - :func:`jax.scipy.special.gammaln`: the natural log of the gamma function
    - :func:`jax.scipy.special.gammasgn`: the sign of the gamma function
    - :func:`jax.scipy.special.loggamma`: the principal branch of the log-gamma function

  Notes:
    ``gammaln`` does not support complex-valued inputs.
  """
  x, = promote_args_inexact("gammaln", x)
  return lax.lgamma(x)

