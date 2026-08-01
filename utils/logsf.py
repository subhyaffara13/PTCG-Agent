
def logsf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
          loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Beta distribution log survival function.

  JAX implementation of :obj:`scipy.stats.beta` ``logsf``.

  The survival function is defined as

  .. math::

     f_{sf}(x, a, b) = 1 - f_{cdf}(x, a, b)

  where :math:`f_{cdf}(x, a, b)` is the beta cumulative distribution function,
  :func:`jax.scipy.stats.beta.cdf`.

  Args:
    x: arraylike, value at which to evaluate the SF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logsf values.

  See Also:
    - :func:`jax.scipy.stats.beta.cdf`
    - :func:`jax.scipy.stats.beta.pdf`
    - :func:`jax.scipy.stats.beta.sf`
    - :func:`jax.scipy.stats.beta.logcdf`
    - :func:`jax.scipy.stats.beta.logpdf`
  """
  return lax.log(sf(x, a, b, loc, scale))


def logsf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy distribution log survival function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``logsf``

  The survival function is defined as

  .. math::

     f_{sf}(x) = 1 - f_{cdf}(x)

  where :math:`f_{cdf}(x)` is the cumulative distribution function,
  :func:`jax.scipy.stats.cauchy.cdf`.

  Args:
    x: arraylike, value at which to evaluate the SF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logsf values.

  See Also:
    - :func:`jax.scipy.stats.cauchy.cdf`
    - :func:`jax.scipy.stats.cauchy.pdf`
    - :func:`jax.scipy.stats.cauchy.sf`
    - :func:`jax.scipy.stats.cauchy.logcdf`
    - :func:`jax.scipy.stats.cauchy.logpdf`
    - :func:`jax.scipy.stats.cauchy.isf`
    - :func:`jax.scipy.stats.cauchy.ppf`
  """
  x, loc, scale = promote_args_inexact("cauchy.logsf", x, loc, scale)
  return logcdf(-x, -loc, scale)


def logsf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Chi-square log survival function.

  JAX implementation of :obj:`scipy.stats.chi2` ``logsf``.

  The survival function is defined as

  .. math::

     f_{sf}(x, k) = 1 - f_{cdf}(x, k)

  where :math:`f_{cdf}(x, k)` is the cumulative distribution function,
  :func:`jax.scipy.stats.chi2.cdf`. JAX follows the scipy
  convention of using ``df`` to denote degrees of freedom.

  Args:
    x: arraylike, value at which to evaluate the SF
    df: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logsf values.

  See Also:
    - :func:`jax.scipy.stats.chi2.cdf`
    - :func:`jax.scipy.stats.chi2.pdf`
    - :func:`jax.scipy.stats.chi2.sf`
    - :func:`jax.scipy.stats.chi2.logcdf`
    - :func:`jax.scipy.stats.chi2.logpdf`
  """
  return lax.log(sf(x, df, loc, scale))


def logsf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Exponential log survival function.

  JAX implementation of :obj:`scipy.stats.expon` ``logsf``.

  The survival function is defined as

  .. math::

     f_{sf}(x) = 1 - f_{cdf}(x)

  where :math:`f_{cdf}(x)` is the exponential cumulative distribution function,
  :func:`jax.scipy.stats.expon.cdf`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of pdf values.

  See Also:
    :func:`jax.scipy.stats.expon.cdf`
    :func:`jax.scipy.stats.expon.pdf`
    :func:`jax.scipy.stats.expon.ppf`
    :func:`jax.scipy.stats.expon.sf`
    :func:`jax.scipy.stats.expon.logcdf`
    :func:`jax.scipy.stats.expon.logpdf`
    :func:`jax.scipy.stats.expon.logsf`
  """
  x, loc, scale = promote_args_inexact("expon.sf", x, loc, scale)
  neg_scaled_x = lax.div(lax.sub(loc, x), scale)
  return jnp.where(lax.lt(x, loc), jnp.zeros_like(neg_scaled_x), neg_scaled_x)


def logsf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Gamma log survival function.

  JAX implementation of :obj:`scipy.stats.gamma` ``logsf``.

  The survival function is defined as

  .. math::

     f_{sf}(x, k) = 1 - f_{cdf}(x, k)

  where :math:`f_{cdf}(x, k)` is the cumulative distribution function,
  :func:`jax.scipy.stats.gamma.cdf`.

  Args:
    x: arraylike, value at which to evaluate the SF
    a: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logsf values.

  See Also:
    - :func:`jax.scipy.stats.gamma.cdf`
    - :func:`jax.scipy.stats.gamma.pdf`
    - :func:`jax.scipy.stats.gamma.sf`
    - :func:`jax.scipy.stats.gamma.logcdf`
    - :func:`jax.scipy.stats.gamma.logpdf`
  """
  return lax.log(sf(x, a, loc, scale))


def logsf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Left Skewed) log survival function.

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``logsf``.

  .. math::

      f_{sf}(x; \mu, \beta) = 1 - f_{cdf}(x, \mu, \beta)

  Args:
    x: ArrayLike, value at which to evaluate log survival function
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of logsf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_l.logpdf`
    - :func:`jax.scipy.stats.gumbel_l.pdf`
    - :func:`jax.scipy.stats.gumbel_l.logcdf`
    - :func:`jax.scipy.stats.gumbel_l.cdf`
    - :func:`jax.scipy.stats.gumbel_l.sf`
  """
  x, loc, scale = promote_args_inexact("gumbel_l.logsf", x, loc, scale)
  ok = lax.gt(scale, _lax_const(scale, 0))
  # logsf = -exp(z)
  z = lax.div(lax.sub(x, loc), scale)
  log_sf = lax.neg(lax.exp(z))
  return jnp.where(ok, log_sf, np.nan)


def logsf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Right Skewed) log survival function.

  JAX implementation of :obj:`scipy.stats.gumbel_r` ``logsf``.

  Args:
    x: ArrayLike, value at which to evaluate log survival function
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of logsf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_r.logpdf`
    - :func:`jax.scipy.stats.gumbel_r.pdf`
    - :func:`jax.scipy.stats.gumbel_r.logcdf`
    - :func:`jax.scipy.stats.gumbel_r.cdf`
    - :func:`jax.scipy.stats.gumbel_r.sf`
  """
  x, loc, scale = promote_args_inexact("gumbel_r.logsf", x, loc, scale)
  ok = lax.gt(scale, _lax_const(scale, 0))
  # logsf = log(1 - exp(-exp(-z)))
  neg_z = lax.div(lax.sub(loc, x), scale)
  log_sf = log1mexp(lax.exp(neg_z))
  return jnp.where(ok, log_sf, np.nan)


def logsf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Normal distribution log survival function.

  JAX implementation of :obj:`scipy.stats.norm` ``logsf``.

  The survival function is defined as

  .. math::

     f_{sf}(x) = 1 - f_{cdf}(x)

  where :math:`f_{cdf}(x)` is the cumulative distribution function,
  :func:`jax.scipy.stats.norm.cdf`.

  Args:
    x: arraylike, value at which to evaluate the SF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logsf values.

  See Also:
    - :func:`jax.scipy.stats.norm.cdf`
    - :func:`jax.scipy.stats.norm.pdf`
    - :func:`jax.scipy.stats.norm.sf`
    - :func:`jax.scipy.stats.norm.logcdf`
    - :func:`jax.scipy.stats.norm.logpdf`
    - :func:`jax.scipy.stats.norm.isf`
    - :func:`jax.scipy.stats.norm.ppf`
  """
  x, loc, scale = promote_args_inexact("norm.logsf", x, loc, scale)
  return logcdf(-x, -loc, scale)


def logsf(
  x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1
) -> Array:
  r"""Pareto log survival function.

  JAX implementation of :obj:`scipy.stats.pareto` ``logsf``.

  The Pareto survival function is given by

  .. math::

     S(x, b) = \begin{cases}
       x^{-b} & x \ge 1\\
       1 & x < 1
     \end{cases}

  and is defined for :math:`b > 0`.

  Args:
    x: arraylike, value at which to evaluate the survival function
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of log survival function values.

  See Also:
    - :func:`jax.scipy.stats.pareto.logcdf`
    - :func:`jax.scipy.stats.pareto.logpdf`
    - :func:`jax.scipy.stats.pareto.cdf`
    - :func:`jax.scipy.stats.pareto.pdf`
    - :func:`jax.scipy.stats.pareto.ppf`
    - :func:`jax.scipy.stats.pareto.sf`
  """
  x, b, loc, scale = promote_args_inexact("pareto.logsf", x, b, loc, scale)
  zero = _lax_const(x, 0)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  logsf_val = lax.neg(lax.mul(b, lax.log(scaled_x)))
  return jnp.where(lax.lt(x, lax.add(loc, scale)), zero, logsf_val)


def logsf(x, a, b, loc=0, scale=1):
  """Truncated normal distribution log survival function.

  JAX implementation of :obj:`scipy.stats.truncnorm` ``logsf``

  The survival function is defined as

  .. math::

     f_{sf}(x) = 1 - f_{cdf}(x)

  where :math:`f_{cdf}(x)` is the cumulative distribution function,
  :func:`jax.scipy.stats.truncnorm.cdf`.

  Args:
    x: arraylike, value at which to evaluate the SF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logsf values.

  See Also:
    - :func:`jax.scipy.stats.truncnorm.cdf`
    - :func:`jax.scipy.stats.truncnorm.pdf`
    - :func:`jax.scipy.stats.truncnorm.sf`
    - :func:`jax.scipy.stats.truncnorm.logcdf`
    - :func:`jax.scipy.stats.truncnorm.logpdf`
  """
  x, a, b, loc, scale = promote_args_inexact("truncnorm.logsf", x, a, b, loc, scale)
  return logcdf(-x, -b, -a, -loc, scale)

