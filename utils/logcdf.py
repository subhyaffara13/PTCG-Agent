
def logcdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
           loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Beta log cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.beta` ``logcdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x, a, b) = \int_{-\infty}^x f_{pdf}(y, a, b)\mathrm{d}y

  where :math:`f_{pdf}` is the beta distribution probability density function,
  :func:`jax.scipy.stats.beta.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logcdf values

  See Also:
    - :func:`jax.scipy.stats.beta.cdf`
    - :func:`jax.scipy.stats.beta.pdf`
    - :func:`jax.scipy.stats.beta.sf`
    - :func:`jax.scipy.stats.beta.logpdf`
    - :func:`jax.scipy.stats.beta.logsf`
  """
  return lax.log(cdf(x, a, b, loc, scale))


def logcdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy log cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``logcdf``

  The cdf is defined as

  .. math::

     f_{cdf} = \int_{-\infty}^x f_{pdf}(y) \mathrm{d}y

  where here :math:`f_{pdf}` is the Cauchy probability distribution function,
  :func:`jax.scipy.stats.cauchy.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logcdf values.

  See Also:
    - :func:`jax.scipy.stats.cauchy.cdf`
    - :func:`jax.scipy.stats.cauchy.pdf`
    - :func:`jax.scipy.stats.cauchy.sf`
    - :func:`jax.scipy.stats.cauchy.logpdf`
    - :func:`jax.scipy.stats.cauchy.logsf`
    - :func:`jax.scipy.stats.cauchy.isf`
    - :func:`jax.scipy.stats.cauchy.ppf`
  """
  return lax.log(cdf(x, loc, scale))


def logcdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Chi-square log cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.chi2` ``logcdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x, k) = \int_{-\infty}^x f_{pdf}(y, k)\mathrm{d}y

  where :math:`f_{pdf}` is the probability density function,
  :func:`jax.scipy.stats.chi2.pdf`. JAX follows the scipy
  convention of using ``df`` to denote degrees of freedom.

  Args:
    x: arraylike, value at which to evaluate the CDF
    df: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logcdf values

  See Also:
    - :func:`jax.scipy.stats.chi2.cdf`
    - :func:`jax.scipy.stats.chi2.pdf`
    - :func:`jax.scipy.stats.chi2.sf`
    - :func:`jax.scipy.stats.chi2.logpdf`
    - :func:`jax.scipy.stats.chi2.logsf`
  """
  return lax.log(cdf(x, df, loc, scale))


def logcdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Exponential log cumulative density function.

  JAX implementation of :obj:`scipy.stats.expon` ``logcdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x) = \int_{-\infty}^x f_{pdf}(y)\mathrm{d}y

  where :math:`f_{pdf}` is the exponential distribution probability density function,
  :func:`jax.scipy.stats.expon.pdf`.

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
  return lax.log1p(lax.neg(sf(x, loc, scale)))


def logcdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Gamma log cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.gamma` ``logcdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x, a) = \int_{-\infty}^x f_{pdf}(y, a)\mathrm{d}y

  where :math:`f_{pdf}` is the probability density function,
  :func:`jax.scipy.stats.gamma.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    a: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logcdf values.

  See Also:
    - :func:`jax.scipy.stats.gamma.cdf`
    - :func:`jax.scipy.stats.gamma.pdf`
    - :func:`jax.scipy.stats.gamma.sf`
    - :func:`jax.scipy.stats.gamma.logpdf`
    - :func:`jax.scipy.stats.gamma.logsf`
  """
  return lax.log(cdf(x, a, loc, scale))


def logcdf(x: ArrayLike,
           loc: ArrayLike = 0,
           scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Left Skewed) log cumulative density function.

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``logcdf``.

  .. math::

      f_{cdf}(x; \mu, \beta) = 1 - \exp\left( -\exp\left( \frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate log(cdf)
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of logcdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_l.logpdf`
    - :func:`jax.scipy.stats.gumbel_l.pdf`
    - :func:`jax.scipy.stats.gumbel_l.cdf`
    - :func:`jax.scipy.stats.gumbel_l.ppf`
    - :func:`jax.scipy.stats.gumbel_l.logsf`
    - :func:`jax.scipy.stats.gumbel_l.sf`
  """
  x, loc, scale = promote_args_inexact("gumbel_l.logcdf", x, loc, scale)
  ok = lax.gt(scale, _lax_const(scale, 0))
  z = lax.div(lax.sub(x, loc), scale)
  neg_exp_z = lax.neg(lax.exp(z))
  # xlog1p fails here, that's why log1p is used here
  # even log1p fails for some cases when using float64 mode
  # so we're using this formula which is stable
  log_cdf = lax.log(-lax.expm1(neg_exp_z))
  return jnp.where(ok, log_cdf, np.nan)


def logcdf(x: ArrayLike,
           loc: ArrayLike = 0,
           scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Right Skewed) log cumulative density function.

  JAX implementation of :obj:`scipy.stats.gumbel_r` ``logcdf``.

  .. math::

      f_{cdf}(x; \mu, \beta) = \exp\left( -\exp\left( -\frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate log(cdf)
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of logcdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_r.logpdf`
    - :func:`jax.scipy.stats.gumbel_r.pdf`
    - :func:`jax.scipy.stats.gumbel_r.cdf`
    - :func:`jax.scipy.stats.gumbel_r.ppf`
    - :func:`jax.scipy.stats.gumbel_r.sf`
    - :func:`jax.scipy.stats.gumbel_r.logsf`
  """
  x, loc, scale = promote_args_inexact("gumbel_r.logcdf", x, loc, scale)
  ok = lax.gt(scale, _lax_const(scale, 0))
  z = lax.div(lax.sub(x, loc), scale)
  # log cdf = -exp(-z)
  log_cdf = lax.neg(lax.exp(lax.neg(z)))
  return jnp.where(ok, log_cdf, np.nan)


def logcdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Normal log cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.norm` ``logcdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x, k) = \int_{-\infty}^x f_{pdf}(y, k)\mathrm{d}y

  where :math:`f_{pdf}` is the probability density function,
  :func:`jax.scipy.stats.norm.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logcdf values.

  See Also:
    - :func:`jax.scipy.stats.norm.cdf`
    - :func:`jax.scipy.stats.norm.pdf`
    - :func:`jax.scipy.stats.norm.sf`
    - :func:`jax.scipy.stats.norm.logpdf`
    - :func:`jax.scipy.stats.norm.logsf`
    - :func:`jax.scipy.stats.norm.isf`
    - :func:`jax.scipy.stats.norm.ppf`
  """
  x, loc, scale = promote_args_inexact("norm.logcdf", x, loc, scale)
  return special.log_ndtr(lax.div(lax.sub(x, loc), scale))


def logcdf(
  x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1
) -> Array:
  r"""Pareto log cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.pareto` ``logcdf``.

  The Pareto cumulative distribution function is given by

  .. math::

     F(x, b) = \begin{cases}
       1 - x^{-b} & x \ge 1\\
       0 & x < 1
     \end{cases}

  and is defined for :math:`b > 0`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logCDF values.

  See Also:
    - :func:`jax.scipy.stats.pareto.logpdf`
    - :func:`jax.scipy.stats.pareto.logsf`
    - :func:`jax.scipy.stats.pareto.cdf`
    - :func:`jax.scipy.stats.pareto.pdf`
    - :func:`jax.scipy.stats.pareto.ppf`
    - :func:`jax.scipy.stats.pareto.sf`
  """
  x, b, loc, scale = promote_args_inexact("pareto.logcdf", x, b, loc, scale)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  logcdf_val = lax.log1p(lax.neg(lax.pow(scaled_x, lax.neg(b))))
  return jnp.where(lax.lt(x, lax.add(loc, scale)), -np.inf, logcdf_val)


def logcdf(x, a, b, loc=0, scale=1):
  r"""Truncated normal log cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.truncnorm` ``logcdf``.

  The cdf is defined as

  .. math::

     f_{cdf} = \int_{-\infty}^x f_{pdf}(y) \mathrm{d}y

  where here :math:`f_{pdf}` is the probability distribution function,
  :func:`jax.scipy.stats.truncnorm.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logcdf values.

  See Also:
    - :func:`jax.scipy.stats.truncnorm.cdf`
    - :func:`jax.scipy.stats.truncnorm.pdf`
    - :func:`jax.scipy.stats.truncnorm.sf`
    - :func:`jax.scipy.stats.truncnorm.logpdf`
    - :func:`jax.scipy.stats.truncnorm.logsf`
  """
  x, a, b, loc, scale = promote_args_inexact("truncnorm.logcdf", x, a, b, loc, scale)
  x, a, b = jnp.broadcast_arrays(x, a, b)
  x = lax.div(lax.sub(x, loc), scale)
  lgm_ab = _log_gauss_mass(a, b)
  logcdf = _log_gauss_mass(a, x) - lgm_ab
  logsf = _log_gauss_mass(x, b) - lgm_ab

  logcdf = jnp.select(
    # third condition: avoid catastrophic cancellation (from scipy)
    [x >= b, x <= a, logcdf > -0.1, x > a],
    [0, -np.inf, jnp.log1p(-jnp.exp(logsf)), logcdf]
  )
  logcdf = jnp.where(a >= b, np.nan, logcdf)
  return logcdf

