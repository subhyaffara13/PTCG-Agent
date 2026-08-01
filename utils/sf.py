
def sf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
       loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Beta distribution survival function.

  JAX implementation of :obj:`scipy.stats.beta` ``sf``.

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
    array of sf values.

  See Also:
    - :func:`jax.scipy.stats.beta.cdf`
    - :func:`jax.scipy.stats.beta.pdf`
    - :func:`jax.scipy.stats.beta.logcdf`
    - :func:`jax.scipy.stats.beta.logpdf`
    - :func:`jax.scipy.stats.beta.logsf`
  """
  x, a, b, loc, scale = promote_args_inexact("beta.sf", x, a, b, loc, scale)
  return betainc(
    b,
    a,
    1 - lax.clamp(
      _lax_const(x, 0),
      lax.div(lax.sub(x, loc), scale),
      _lax_const(x, 1),
    )
  )


def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy distribution log survival function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``sf``.

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
    array of sf values

  See Also:
    - :func:`jax.scipy.stats.cauchy.cdf`
    - :func:`jax.scipy.stats.cauchy.pdf`
    - :func:`jax.scipy.stats.cauchy.logcdf`
    - :func:`jax.scipy.stats.cauchy.logpdf`
    - :func:`jax.scipy.stats.cauchy.logsf`
    - :func:`jax.scipy.stats.cauchy.isf`
    - :func:`jax.scipy.stats.cauchy.ppf`
  """
  x, loc, scale = promote_args_inexact("cauchy.sf", x, loc, scale)
  return cdf(-x, -loc, scale)


def sf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Chi-square survival function.

  JAX implementation of :obj:`scipy.stats.chi2` ``sf``.

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
    array of sf values.

  See Also:
    - :func:`jax.scipy.stats.chi2.cdf`
    - :func:`jax.scipy.stats.chi2.pdf`
    - :func:`jax.scipy.stats.chi2.logcdf`
    - :func:`jax.scipy.stats.chi2.logpdf`
    - :func:`jax.scipy.stats.chi2.logsf`
  """
  x, df, loc, scale = promote_args_inexact("chi2.sf", x, df, loc, scale)
  two = _lax_const(scale, 2)
  return gammaincc(
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


def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Exponential survival function.

  JAX implementation of :obj:`scipy.stats.expon` ``sf``.

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
  return lax.exp(logsf(x, loc, scale))


def sf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Gamma survival function.

  JAX implementation of :obj:`scipy.stats.gamma` ``sf``.

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
    array of sf values.

  See Also:
    - :func:`jax.scipy.stats.gamma.cdf`
    - :func:`jax.scipy.stats.gamma.pdf`
    - :func:`jax.scipy.stats.gamma.logcdf`
    - :func:`jax.scipy.stats.gamma.logpdf`
    - :func:`jax.scipy.stats.gamma.logsf`
  """
  x, a, loc, scale = promote_args_inexact("gamma.sf", x, a, loc, scale)
  y = lax.div(lax.sub(x, loc), scale)
  return jnp.where(lax.lt(y, _lax_const(y, 0)), 1, gammaincc(a, y))


def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Left Skewed) survival function.

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``sf``.

  .. math::

      f_{sf}(x; \mu, \beta) = 1 - f_{cdf}(x, \mu, \beta)

  Args:
    x: ArrayLike, value at which to evaluate survival function
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of sf values (1 - cdf)

  See Also:
    - :func:`jax.scipy.stats.gumbel_l.logpdf`
    - :func:`jax.scipy.stats.gumbel_l.pdf`
    - :func:`jax.scipy.stats.gumbel_l.logcdf`
    - :func:`jax.scipy.stats.gumbel_l.cdf`
    - :func:`jax.scipy.stats.gumbel_l.logsf`
  """
  return jnp.exp(logsf(x, loc, scale))


def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Right Skewed) survival function.

  JAX implementation of :obj:`scipy.stats.gumbel_r` ``sf``.

  .. math::

      f_{sf}(x; \mu, \beta) = 1 - F_{cdf}(x; \mu, \beta)

  Args:
    x: ArrayLike, value at which to evaluate survival function
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of sf values (1 - cdf)

  See Also:
    - :func:`jax.scipy.stats.gumbel_r.logpdf`
    - :func:`jax.scipy.stats.gumbel_r.pdf`
    - :func:`jax.scipy.stats.gumbel_r.logcdf`
    - :func:`jax.scipy.stats.gumbel_r.cdf`
    - :func:`jax.scipy.stats.gumbel_r.logsf`
  """
  x, loc, scale = promote_args_inexact("gumbel_r.sf", x, loc, scale)
  ok = lax.gt(scale, _lax_const(scale, 0))
  # sf = 1 - exp(-exp(-z))
  neg_z = lax.div(lax.sub(loc, x), scale)
  t1 = lax.exp(lax.neg(lax.exp(neg_z)))
  _sf = lax.sub(_lax_const(x, 1), t1)
  return jnp.where(ok, _sf, np.nan)


def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Logistic distribution survival function.

  JAX implementation of :obj:`scipy.stats.logistic` ``sf``

  The survival function is defined as

  .. math::

     f_{sf}(x, k) = 1 - f_{cdf}(x, k)

  where :math:`f_{cdf}(x, k)` is the cumulative distribution function,
  :func:`jax.scipy.stats.logistic.cdf`.

  Args:
    x: arraylike, value at which to evaluate the SF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of sf values.

  See Also:
    - :func:`jax.scipy.stats.logistic.cdf`
    - :func:`jax.scipy.stats.logistic.pdf`
    - :func:`jax.scipy.stats.logistic.isf`
    - :func:`jax.scipy.stats.logistic.logpdf`
    - :func:`jax.scipy.stats.logistic.ppf`
  """
  x, loc, scale = promote_args_inexact("logistic.sf", x, loc, scale)
  return expit(lax.neg(lax.div(lax.sub(x, loc), scale)))


def sf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Normal distribution survival function.

  JAX implementation of :obj:`scipy.stats.norm` ``sf``.

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
    array of sf values.

  See Also:
    - :func:`jax.scipy.stats.norm.cdf`
    - :func:`jax.scipy.stats.norm.pdf`
    - :func:`jax.scipy.stats.norm.logcdf`
    - :func:`jax.scipy.stats.norm.logpdf`
    - :func:`jax.scipy.stats.norm.logsf`
    - :func:`jax.scipy.stats.norm.isf`
    - :func:`jax.scipy.stats.norm.ppf`
  """
  x, loc, scale = promote_args_inexact("norm.sf", x, loc, scale)
  return cdf(-x, -loc, scale)


def sf(
  x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1
) -> Array:
  r"""Pareto survival function.

  JAX implementation of :obj:`scipy.stats.pareto` ``sf``.

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
    array of survival function values.

  See Also:
    - :func:`jax.scipy.stats.pareto.logcdf`
    - :func:`jax.scipy.stats.pareto.logpdf`
    - :func:`jax.scipy.stats.pareto.logsf`
    - :func:`jax.scipy.stats.pareto.cdf`
    - :func:`jax.scipy.stats.pareto.pdf`
    - :func:`jax.scipy.stats.pareto.ppf`
  """
  return lax.exp(logsf(x, b, loc, scale))


def sf(x, a, b, loc=0, scale=1):
  """Truncated normal distribution survival function.

  JAX implementation of :obj:`scipy.stats.truncnorm` ``sf``

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
    array of sf values.

  See Also:
    - :func:`jax.scipy.stats.truncnorm.cdf`
    - :func:`jax.scipy.stats.truncnorm.pdf`
    - :func:`jax.scipy.stats.truncnorm.sf`
    - :func:`jax.scipy.stats.truncnorm.logcdf`
    - :func:`jax.scipy.stats.truncnorm.logpdf`
  """
  return lax.exp(logsf(x, a, b, loc, scale))

