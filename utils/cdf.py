
def cdf(expr, condition=None, evaluate=True, **kwargs):
    """
    Cumulative Distribution Function of a random expression.

    optionally given a second condition.

    Explanation
    ===========

    This density will take on different forms for different types of
    probability spaces.
    Discrete variables produce Dicts.
    Continuous variables produce Lambdas.

    Examples
    ========

    >>> from sympy.stats import density, Die, Normal, cdf

    >>> D = Die('D', 6)
    >>> X = Normal('X', 0, 1)

    >>> density(D).dict
    {1: 1/6, 2: 1/6, 3: 1/6, 4: 1/6, 5: 1/6, 6: 1/6}
    >>> cdf(D)
    {1: 1/6, 2: 1/3, 3: 1/2, 4: 2/3, 5: 5/6, 6: 1}
    >>> cdf(3*D, D > 2)
    {9: 1/4, 12: 1/2, 15: 3/4, 18: 1}

    >>> cdf(X)
    Lambda(_z, erf(sqrt(2)*_z/2)/2 + 1/2)
    """
    if condition is not None:  # If there is a condition
        # Recompute on new conditional expr
        return cdf(given(expr, condition, **kwargs), **kwargs)

    # Otherwise pass work off to the ProbabilitySpace
    result = pspace(expr).compute_cdf(expr, **kwargs)

    if evaluate and hasattr(result, 'doit'):
        return result.doit()
    else:
        return result


def cdf(k: ArrayLike, p: ArrayLike) -> Array:
  r"""Bernoulli cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.bernoulli` ``cdf``

  The Bernoulli cumulative distribution function is defined as:

  .. math::

     f_{cdf}(k, p) = \sum_{i=0}^k f_{pmf}(k, p)

  where :math:`f_{pmf}(k, p)` is the Bernoulli probability mass function
  :func:`jax.scipy.stats.bernoulli.pmf`.

  Args:
    k: arraylike, value at which to evaluate the CDF
    p: arraylike, distribution shape parameter

  Returns:
    array of cdf values

  See Also:
    - :func:`jax.scipy.stats.bernoulli.logpmf`
    - :func:`jax.scipy.stats.bernoulli.pmf`
    - :func:`jax.scipy.stats.bernoulli.ppf`
  """
  k, p = promote_args_inexact('bernoulli.cdf', k, p)
  zero, one = _lax_const(k, 0), _lax_const(k, 1)
  conds = [
    jnp.isnan(k) | jnp.isnan(p) | (p < zero) | (p > one),
    lax.lt(k, zero),
    jnp.logical_and(lax.ge(k, zero), lax.lt(k, one)),
    lax.ge(k, one)
    ]
  vals = [jnp.nan, zero, one - p, one]
  return jnp.select(conds, vals)


def cdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
        loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Beta cumulative distribution function

  JAX implementation of :obj:`scipy.stats.beta` ``cdf``.

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
    array of cdf values

  See Also:
    - :func:`jax.scipy.stats.beta.pdf`
    - :func:`jax.scipy.stats.beta.sf`
    - :func:`jax.scipy.stats.beta.logcdf`
    - :func:`jax.scipy.stats.beta.logpdf`
    - :func:`jax.scipy.stats.beta.logsf`
  """
  x, a, b, loc, scale = promote_args_inexact("beta.cdf", x, a, b, loc, scale)
  return betainc(
    a,
    b,
    lax.clamp(
      _lax_const(x, 0),
      lax.div(lax.sub(x, loc), scale),
      _lax_const(x, 1),
    )
  )


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``cdf``.

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
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.cauchy.pdf`
    - :func:`jax.scipy.stats.cauchy.sf`
    - :func:`jax.scipy.stats.cauchy.logcdf`
    - :func:`jax.scipy.stats.cauchy.logpdf`
    - :func:`jax.scipy.stats.cauchy.logsf`
    - :func:`jax.scipy.stats.cauchy.isf`
    - :func:`jax.scipy.stats.cauchy.ppf`
  """
  x, loc, scale = promote_args_inexact("cauchy.cdf", x, loc, scale)
  pi = _lax_const(x, np.pi)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  return lax.add(_lax_const(x, 0.5), lax.mul(lax.div(_lax_const(x, 1.), pi), arctan(scaled_x)))


def cdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Chi-square cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.chi2` ``cdf``.

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
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.chi2.pdf`
    - :func:`jax.scipy.stats.chi2.sf`
    - :func:`jax.scipy.stats.chi2.logcdf`
    - :func:`jax.scipy.stats.chi2.logpdf`
    - :func:`jax.scipy.stats.chi2.logsf`
  """
  x, df, loc, scale = promote_args_inexact("chi2.cdf", x, df, loc, scale)
  two = _lax_const(scale, 2)
  return gammainc(
    lax.div(df, two),
    lax.clamp(
      _lax_const(x, 0),
      lax.div(
        lax.sub(x, loc),
        lax.mul(scale, two),
      ),
      _lax_const(x, np.inf),
    ),
  )


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Exponential cumulative density function.

  JAX implementation of :obj:`scipy.stats.expon` ``cdf``.

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
  x, loc, scale = promote_args_inexact("expon.cdf", x, loc, scale)
  neg_scaled_x = lax.div(lax.sub(loc, x), scale)
  return jnp.where(
    lax.lt(x, loc),
    jnp.zeros_like(neg_scaled_x),
    lax.neg(lax.expm1(neg_scaled_x)),
  )


def cdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Gamma cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.gamma` ``cdf``.

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
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.gamma.pdf`
    - :func:`jax.scipy.stats.gamma.sf`
    - :func:`jax.scipy.stats.gamma.logcdf`
    - :func:`jax.scipy.stats.gamma.logpdf`
    - :func:`jax.scipy.stats.gamma.logsf`
  """
  x, a, loc, scale = promote_args_inexact("gamma.cdf", x, a, loc, scale)
  return gammainc(
    a,
    lax.clamp(
      _lax_const(x, 0),
      lax.div(lax.sub(x, loc), scale),
      _lax_const(x, np.inf),
    )
  )


def cdf(x: ArrayLike, beta: ArrayLike) -> Array:
  r"""Generalized normal cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.gennorm` ``cdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x, k) = \int_{-\infty}^x f_{pdf}(y, k)\mathrm{d}y

  where :math:`f_{pdf}` is the probability density function,
  :func:`jax.scipy.stats.gennorm.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    beta: arraylike, distribution shape parameter

  Returns:
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.gennorm.pdf`
    - :func:`jax.scipy.stats.gennorm.logpdf`
  """
  x, beta = promote_args_inexact("gennorm.cdf", x, beta)
  return .5 * (1 + lax.sign(x) * lax.igamma(1/beta, lax.abs(x)**beta))


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Left Skewed) cumulative density function.

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``cdf``.

  .. math::

      f_{cdf}(x; \mu, \beta) = 1 - \exp\left( -\exp\left( \frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate cdf
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of cdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_l.logpdf`
    - :func:`jax.scipy.stats.gumbel_l.pdf`
    - :func:`jax.scipy.stats.gumbel_l.logcdf`
    - :func:`jax.scipy.stats.gumbel_l.ppf`
    - :func:`jax.scipy.stats.gumbel_l.logsf`
    - :func:`jax.scipy.stats.gumbel_l.sf`
  """
  return lax.exp(logcdf(x, loc, scale))


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Right Skewed) cumulative density function.

  JAX implementation of :obj:`scipy.stats.gumbel_r` ``cdf``.

  .. math::

      f_{cdf}(x; \mu, \beta) = \exp\left( -\exp\left( -\frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate cdf
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of cdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_r.logpdf`
    - :func:`jax.scipy.stats.gumbel_r.pdf`
    - :func:`jax.scipy.stats.gumbel_r.logcdf`
    - :func:`jax.scipy.stats.gumbel_r.ppf`
    - :func:`jax.scipy.stats.gumbel_r.sf`
    - :func:`jax.scipy.stats.gumbel_r.logsf`
  """
  return lax.exp(logcdf(x, loc, scale))


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Laplace cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.laplace` ``cdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x, k) = \int_{-\infty}^x f_{pdf}(y, k)\mathrm{d}y

  where :math:`f_{pdf}` is the probability density function,
  :func:`jax.scipy.stats.laplace.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.laplace.pdf`
    - :func:`jax.scipy.stats.laplace.logpdf`
  """
  x, loc, scale = promote_args_inexact("laplace.cdf", x, loc, scale)
  half = _lax_const(x, 0.5)
  one = _lax_const(x, 1)
  zero = _lax_const(x, 0)
  diff = lax.div(lax.sub(x, loc), scale)
  return lax.select(lax.le(diff, zero),
                    lax.mul(half, lax.exp(diff)),
                    lax.sub(one, lax.mul(half, lax.exp(lax.neg(diff)))))


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Logistic cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.logistic` ``cdf``.

  The cdf is defined as

  .. math::

     f_{cdf}(x, k) = \int_{-\infty}^x f_{pdf}(y, k)\mathrm{d}y

  where :math:`f_{pdf}` is the probability density function,
  :func:`jax.scipy.stats.logistic.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.logistic.pdf`
    - :func:`jax.scipy.stats.logistic.sf`
    - :func:`jax.scipy.stats.logistic.isf`
    - :func:`jax.scipy.stats.logistic.logpdf`
    - :func:`jax.scipy.stats.logistic.ppf`
  """
  x, loc, scale = promote_args_inexact("logistic.cdf", x, loc, scale)
  return expit(lax.div(lax.sub(x, loc), scale))


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Normal cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.norm` ``cdf``.

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
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.norm.pdf`
    - :func:`jax.scipy.stats.norm.sf`
    - :func:`jax.scipy.stats.norm.logcdf`
    - :func:`jax.scipy.stats.norm.logpdf`
    - :func:`jax.scipy.stats.norm.logsf`
    - :func:`jax.scipy.stats.norm.isf`
    - :func:`jax.scipy.stats.norm.ppf`
  """
  x, loc, scale = promote_args_inexact("norm.cdf", x, loc, scale)
  return special.ndtr(lax.div(lax.sub(x, loc), scale))


def cdf(
  x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1
) -> Array:
  r"""Pareto cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.pareto` ``cdf``.

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
    array of CDF values.

  See Also:
    - :func:`jax.scipy.stats.pareto.logcdf`
    - :func:`jax.scipy.stats.pareto.logpdf`
    - :func:`jax.scipy.stats.pareto.logsf`
    - :func:`jax.scipy.stats.pareto.pdf`
    - :func:`jax.scipy.stats.pareto.ppf`
    - :func:`jax.scipy.stats.pareto.sf`
  """
  x, b, loc, scale = promote_args_inexact("pareto.cdf", x, b, loc, scale)
  one = _lax_const(x, 1)
  zero = _lax_const(x, 0)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  cdf = lax.sub(one, lax.pow(scaled_x, lax.neg(b)))
  return jnp.where(lax.lt(x, lax.add(loc, scale)), zero, cdf)


def cdf(k: ArrayLike, mu: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Poisson cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.poisson` ``cdf``.

  The cumulative distribution function is defined as:

  .. math::

     f_{cdf}(k, \mu) = \sum_{i=0}^k f_{pmf}(k, \mu)

  where :math:`f_{pmf}(k, \mu)` is the probability mass function
  :func:`jax.scipy.stats.poisson.pmf`.

  Args:
    k: arraylike, value at which to evaluate the CDF
    mu: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.poisson.pmf`
    - :func:`jax.scipy.stats.poisson.logpmf`
    - :func:`jax.scipy.stats.poisson.entropy`
  """
  k, mu, loc = promote_args_inexact("poisson.logpmf", k, mu, loc)
  zero = _lax_const(k, 0)
  x = lax.sub(k, loc)
  p = gammaincc(jnp.floor(1 + x), mu)
  return jnp.where(lax.lt(x, zero), zero, p)


def cdf(x, a, b, loc=0, scale=1):
  r"""Truncated normal cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.truncnorm` ``cdf``.

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
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.truncnorm.pdf`
    - :func:`jax.scipy.stats.truncnorm.sf`
    - :func:`jax.scipy.stats.truncnorm.logcdf`
    - :func:`jax.scipy.stats.truncnorm.logpdf`
    - :func:`jax.scipy.stats.truncnorm.logsf`
  """
  return lax.exp(logcdf(x, a, b, loc, scale))


def cdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Uniform cumulative distribution function.

  JAX implementation of :obj:`scipy.stats.uniform` ``cdf``.

  The cdf is defined as

  .. math::

     f_{cdf} = \int_{-\infty}^x f_{pdf}(y) \mathrm{d}y

  where here :math:`f_{pdf}` is the probability distribution function,
  :func:`jax.scipy.stats.uniform.pdf`.

  Args:
    x: arraylike, value at which to evaluate the CDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of cdf values.

  See Also:
    - :func:`jax.scipy.stats.uniform.pdf`
    - :func:`jax.scipy.stats.uniform.logpdf`
    - :func:`jax.scipy.stats.uniform.ppf`
  """
  x, loc, scale = promote_args_inexact("uniform.cdf", x, loc, scale)
  zero, one = jnp.array(0, x.dtype), jnp.array(1, x.dtype)
  conds = [lax.lt(x, loc), lax.gt(x, lax.add(loc, scale)), lax.ge(x, loc) & lax.le(x, lax.add(loc, scale))]
  vals = [zero, one, lax.div(lax.sub(x, loc), scale)]

  return jnp.select(conds, vals)

