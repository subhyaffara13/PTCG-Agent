
def isf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy distribution inverse survival function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``isf``.

  Returns the inverse of the survival function,
  :func:`jax.scipy.stats.cauchy.sf`.

  Args:
    q: arraylike, value at which to evaluate the ISF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of isf values.

  See Also:
    - :func:`jax.scipy.stats.cauchy.cdf`
    - :func:`jax.scipy.stats.cauchy.pdf`
    - :func:`jax.scipy.stats.cauchy.sf`
    - :func:`jax.scipy.stats.cauchy.logcdf`
    - :func:`jax.scipy.stats.cauchy.logpdf`
    - :func:`jax.scipy.stats.cauchy.logsf`
    - :func:`jax.scipy.stats.cauchy.ppf`
  """
  q, loc, scale = promote_args_inexact("cauchy.isf", q, loc, scale)
  pi = _lax_const(q, np.pi)
  half_pi = _lax_const(q, np.pi / 2)
  unscaled = lax.tan(lax.sub(half_pi, lax.mul(pi, q)))
  return lax.add(lax.mul(unscaled, scale), loc)


def isf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Logistic distribution inverse survival function.

  JAX implementation of :obj:`scipy.stats.logistic` ``isf``.

  Returns the inverse of the survival function,
  :func:`jax.scipy.stats.logistic.sf`.

  Args:
    x: arraylike, value at which to evaluate the ISF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of isf values.

  See Also:
    - :func:`jax.scipy.stats.logistic.cdf`
    - :func:`jax.scipy.stats.logistic.pdf`
    - :func:`jax.scipy.stats.logistic.sf`
    - :func:`jax.scipy.stats.logistic.logpdf`
    - :func:`jax.scipy.stats.logistic.ppf`
  """
  x, loc, scale = promote_args_inexact("logistic.isf", x, loc, scale)
  return lax.add(lax.mul(lax.neg(logit(x)), scale), loc)


def isf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Normal distribution inverse survival function.

  JAX implementation of :obj:`scipy.stats.norm` ``isf``.

  Returns the inverse of the survival function,
  :func:`jax.scipy.stats.norm.sf`.

  Args:
    q: arraylike, value at which to evaluate the ISF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of isf values.

  See Also:
    - :func:`jax.scipy.stats.norm.cdf`
    - :func:`jax.scipy.stats.norm.pdf`
    - :func:`jax.scipy.stats.norm.sf`
    - :func:`jax.scipy.stats.norm.logcdf`
    - :func:`jax.scipy.stats.norm.logpdf`
    - :func:`jax.scipy.stats.norm.logsf`
    - :func:`jax.scipy.stats.norm.ppf`
  """
  return ppf(lax.sub(_lax_const(q, 1), q), loc, scale)

