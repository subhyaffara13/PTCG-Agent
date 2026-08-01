
def ppf(q: ArrayLike, p: ArrayLike) -> Array:
  """Bernoulli percent point function.

  JAX implementation of :obj:`scipy.stats.bernoulli` ``ppf``

  The percent point function is the inverse of the cumulative
  distribution function, :func:`jax.scipy.stats.bernoulli.cdf`.

  Args:
    q: arraylike, value at which to evaluate the PPF
    p: arraylike, distribution shape parameter

  Returns:
    array of ppf values

  See Also:
    - :func:`jax.scipy.stats.bernoulli.cdf`
    - :func:`jax.scipy.stats.bernoulli.logpmf`
    - :func:`jax.scipy.stats.bernoulli.pmf`
  """
  q, p = promote_args_inexact('bernoulli.ppf', q, p)
  zero, one = _lax_const(q, 0), _lax_const(q, 1)
  return jnp.where(
    jnp.isnan(q) | jnp.isnan(p) | (p < zero) | (p > one) | (q < zero) | (q > one),
    jnp.nan,
    jnp.where(lax.le(q, one - p), zero, one)
  )


def ppf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy distribution percent point function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``ppf``.

  The percent point function is defined as the inverse of the
  cumulative distribution function, :func:`jax.scipy.stats.cauchy.cdf`.

  Args:
    q: arraylike, value at which to evaluate the PPF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of ppf values.

  See Also:
    - :func:`jax.scipy.stats.cauchy.cdf`
    - :func:`jax.scipy.stats.cauchy.pdf`
    - :func:`jax.scipy.stats.cauchy.sf`
    - :func:`jax.scipy.stats.cauchy.logcdf`
    - :func:`jax.scipy.stats.cauchy.logpdf`
    - :func:`jax.scipy.stats.cauchy.logsf`
    - :func:`jax.scipy.stats.cauchy.isf`
  """
  q, loc, scale = promote_args_inexact("cauchy.ppf", q, loc, scale)
  pi = _lax_const(q, np.pi)
  half_pi = _lax_const(q, np.pi / 2)
  unscaled = lax.tan(lax.sub(lax.mul(pi, q), half_pi))
  return lax.add(lax.mul(unscaled, scale), loc)


def ppf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Exponential percent point function.

  JAX implementation of :obj:`scipy.stats.expon` ``ppf``.

  The percent point function is defined as the inverse of the
  cumulative distribution function, :func:`jax.scipy.stats.expon.cdf`.

  Args:
    q: arraylike, value at which to evaluate the PPF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of ppf values.

  See Also:
    :func:`jax.scipy.stats.expon.cdf`
    :func:`jax.scipy.stats.expon.pdf`
    :func:`jax.scipy.stats.expon.ppf`
    :func:`jax.scipy.stats.expon.sf`
    :func:`jax.scipy.stats.expon.logcdf`
    :func:`jax.scipy.stats.expon.logpdf`
    :func:`jax.scipy.stats.expon.logsf`
  """
  q, loc, scale = promote_args_inexact("expon.ppf", q, loc, scale)
  return jnp.where(
    jnp.isnan(q) | (q < 0) | (q > 1),
    np.nan,
    lax.sub(loc, lax.mul(scale, lax.log1p(lax.neg(q)))),
  )


def ppf(p: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Left Skewed) percent point function (inverse of CDF)

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``ppf``.

  .. math::

      F_{ppf}}(p; \mu, \beta) = \mu + \beta \log\left( -\log(1 - p) \right)

  Args:
    p: ArrayLike, probability value (quantile) at which to evaluate ppf
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of ppf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_l.logpdf`
    - :func:`jax.scipy.stats.gumbel_l.pdf`
    - :func:`jax.scipy.stats.gumbel_l.logcdf`
    - :func:`jax.scipy.stats.gumbel_l.cdf`
    - :func:`jax.scipy.stats.gumbel_l.logsf`
    - :func:`jax.scipy.stats.gumbel_l.sf`
  """
  p, loc, scale = promote_args_inexact("gumbel_l.ppf", p, loc, scale)
  ok = lax.bitwise_and(lax.gt(p, _lax_const(p, 0)),
                       lax.lt(p, _lax_const(p, 1)))
  # quantile = loc + (scale)*log(-log(1 - p))
  t1 = xlog1py(-1, lax.neg(p))
  # xlogp failed here too, that's why log is used
  t = lax.mul(scale, lax.log(t1))
  quantile = lax.add(loc, t)
  return jnp.where(ok, quantile, np.nan)


def ppf(p: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Right Skewed) percent point function.

  JAX implementation of :obj:`scipy.stats.gumbel_r` ``ppf``.

  .. math::

      F(p; \mu, \beta) = \mu - \beta \log\left( -\log(p) \right)

  Args:
    p: ArrayLike, probability value (quantile) at which to evaluate ppf
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of ppf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_r.logpdf`
    - :func:`jax.scipy.stats.gumbel_r.pdf`
    - :func:`jax.scipy.stats.gumbel_r.logcdf`
    - :func:`jax.scipy.stats.gumbel_r.cdf`
    - :func:`jax.scipy.stats.gumbel_r.sf`
    - :func:`jax.scipy.stats.gumbel_r.logsf`
  """
  p, loc, scale = promote_args_inexact("gumbel_r.ppf", p, loc, scale)
  # 0 < p < 1
  ok = lax.bitwise_and(lax.gt(p, _lax_const(p, 0)),
                       lax.lt(p, _lax_const(p, 1)))

  # quantile = loc - (scale)*log(-log(p))
  t1 = xlogy(-1, p)
  t = lax.mul(scale, lax.log(t1))
  quantile = lax.sub(loc, t)
  return jnp.where(ok, quantile, np.nan)


def ppf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Logistic distribution percent point function.

  JAX implementation of :obj:`scipy.stats.logistic` ``ppf``.

  The percent point function is defined as the inverse of the
  cumulative distribution function, :func:`jax.scipy.stats.logistic.cdf`.

  Args:
    x: arraylike, value at which to evaluate the PPF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of ppf values.

  See Also:
    - :func:`jax.scipy.stats.logistic.cdf`
    - :func:`jax.scipy.stats.logistic.pdf`
    - :func:`jax.scipy.stats.logistic.sf`
    - :func:`jax.scipy.stats.logistic.isf`
    - :func:`jax.scipy.stats.logistic.logpdf`
  """
  x, loc, scale = promote_args_inexact("logistic.ppf", x, loc, scale)
  return lax.add(lax.mul(logit(x), scale), loc)


def ppf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Normal distribution percent point function.

  JAX implementation of :obj:`scipy.stats.norm` ``ppf``.

  The percent point function is defined as the inverse of the
  cumulative distribution function, :func:`jax.scipy.stats.norm.cdf`.

  Args:
    q: arraylike, value at which to evaluate the PPF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of ppf values.

  See Also:
    - :func:`jax.scipy.stats.norm.cdf`
    - :func:`jax.scipy.stats.norm.pdf`
    - :func:`jax.scipy.stats.norm.sf`
    - :func:`jax.scipy.stats.norm.logcdf`
    - :func:`jax.scipy.stats.norm.logpdf`
    - :func:`jax.scipy.stats.norm.logsf`
    - :func:`jax.scipy.stats.norm.isf`
  """
  return jnp.asarray(special.ndtri(q) * scale + loc, float)


def ppf(
  q: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1
) -> Array:
  r"""Pareto percent point function (inverse CDF).

  JAX implementation of :obj:`scipy.stats.pareto` ``ppf``.

  The Pareto percent point function is the inverse of the Pareto CDF, and is
  given by

  .. math::

     F^{-1}(q, b) = \begin{cases}
       (1 - q)^{-1/b} & 0 \le q < 1\\
       \text{NaN} & \text{otherwise}
     \end{cases}

  and is defined for :math:`b > 0`.

  Args:
    q: arraylike, value at which to evaluate the inverse CDF
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of percent point function values.

  See Also:
    - :func:`jax.scipy.stats.pareto.logcdf`
    - :func:`jax.scipy.stats.pareto.logpdf`
    - :func:`jax.scipy.stats.pareto.logsf`
    - :func:`jax.scipy.stats.pareto.cdf`
    - :func:`jax.scipy.stats.pareto.pdf`
    - :func:`jax.scipy.stats.pareto.sf`
  """
  q, b, loc, scale = promote_args_inexact("pareto.ppf", q, b, loc, scale)
  one = _lax_const(q, 1)
  ppf_val = lax.add(
    loc, lax.mul(scale, lax.pow(lax.sub(one, q), lax.neg(lax.div(one, b))))
  )
  return jnp.where(jnp.isnan(q) | (q < 0) | (q > 1), np.nan, ppf_val)


def ppf(q: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  """Uniform distribution percent point function.

  JAX implementation of :obj:`scipy.stats.uniform` ``ppf``.

  The percent point function is defined as the inverse of the
  cumulative distribution function, :func:`jax.scipy.stats.uniform.cdf`.

  Args:
    q: arraylike, value at which to evaluate the PPF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of ppf values.

  See Also:
    - :func:`jax.scipy.stats.uniform.cdf`
    - :func:`jax.scipy.stats.uniform.pdf`
    - :func:`jax.scipy.stats.uniform.logpdf`
  """
  q, loc, scale = promote_args_inexact("uniform.ppf", q, loc, scale)
  return jnp.where(
    jnp.isnan(q) | (q < 0) | (q > 1),
    np.nan,
    lax.add(loc, lax.mul(scale, q))
  )

