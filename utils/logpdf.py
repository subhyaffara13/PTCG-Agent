
def logpdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
           loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Beta log probability distribution function.

  JAX implementation of :obj:`scipy.stats.beta` ``logpdf``.

  The pdf of the beta function is:

  .. math::

    f(x, a, b) = \frac{\Gamma(a + b)}{\Gamma(a)\Gamma(b)} x^{a-1}(1-x)^{b-1}

  where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function,
  It is defined for :math:`0\le x\le 1` and :math:`b>0`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values

  See Also:
    - :func:`jax.scipy.stats.beta.cdf`
    - :func:`jax.scipy.stats.beta.pdf`
    - :func:`jax.scipy.stats.beta.sf`
    - :func:`jax.scipy.stats.beta.logcdf`
    - :func:`jax.scipy.stats.beta.logsf`
  """
  x, a, b, loc, scale = promote_args_inexact("beta.logpdf", x, a, b, loc, scale)
  one = _lax_const(x, 1)
  zero = _lax_const(a, 0)
  shape_term = lax.neg(betaln(a, b))
  y = lax.div(lax.sub(x, loc), scale)
  log_linear_term = lax.add(xlogy(lax.sub(a, one), y),
                            xlog1py(lax.sub(b, one), lax.neg(y)))
  log_probs = lax.sub(lax.add(shape_term, log_linear_term), lax.log(scale))
  result = jnp.where(jnp.logical_or(lax.gt(x, lax.add(loc, scale)),
                                    lax.lt(x, loc)), -np.inf, log_probs)
  result_positive_constants = jnp.where(jnp.logical_or(jnp.logical_or(lax.le(a, zero), lax.le(b, zero)),
                                                       lax.le(scale, zero)), np.nan, result)
  return result_positive_constants


def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy log probability distribution function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``logpdf``.

  The Cauchy probability distribution function is

  .. math::

     f(x) = \frac{1}{\pi(1 + x^2)}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values

  See Also:
    - :func:`jax.scipy.stats.cauchy.cdf`
    - :func:`jax.scipy.stats.cauchy.pdf`
    - :func:`jax.scipy.stats.cauchy.sf`
    - :func:`jax.scipy.stats.cauchy.logcdf`
    - :func:`jax.scipy.stats.cauchy.logsf`
    - :func:`jax.scipy.stats.cauchy.isf`
    - :func:`jax.scipy.stats.cauchy.ppf`
  """
  x, loc, scale = promote_args_inexact("cauchy.logpdf", x, loc, scale)
  pi = _lax_const(x, np.pi)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.mul(pi, scale))
  return lax.neg(lax.add(normalize_term, lax.log1p(lax.mul(scaled_x, scaled_x))))


def logpdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Chi-square log probability distribution function.

  JAX implementation of :obj:`scipy.stats.chi2` ``logpdf``.

  The chi-square probability distribution function is given by:

  .. math::

     f(x, k) = \begin{cases}
       \frac{x^{k/2-1}e^{-x/2}}{2^{k/2}\Gamma(k/2)} & x \ge 0 \\
       0 & \mathrm{otherwise}
     \end{cases}

  for :math:`k` degrees of freedom, and where :math:`\Gamma` is the
  :func:`~jax.scipy.special.gamma` function. JAX follows the scipy
  convention of using ``df`` to denote degrees of freedom.

  Args:
    x: arraylike, value at which to evaluate the PDF
    df: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.chi2.cdf`
    - :func:`jax.scipy.stats.chi2.pdf`
    - :func:`jax.scipy.stats.chi2.sf`
    - :func:`jax.scipy.stats.chi2.logcdf`
    - :func:`jax.scipy.stats.chi2.logsf`
  """
  x, df, loc, scale = promote_args_inexact("chi2.logpdf", x, df, loc, scale)
  one = _lax_const(x, 1)
  two = _lax_const(x, 2)
  y = lax.div(lax.sub(x, loc), scale)
  df_on_two = lax.div(df, two)

  kernel = lax.sub(lax.mul(lax.sub(df_on_two, one), lax.log(y)), lax.div(y,two))

  nrml_cnst = lax.neg(lax.add(lax.lgamma(df_on_two),lax.div(lax.mul(lax.log(two), df),two)))

  log_probs = lax.add(lax.sub(nrml_cnst, lax.log(scale)), kernel)
  return jnp.where(lax.lt(x, loc), -np.inf, log_probs)


def logpdf(x: ArrayLike, alpha: ArrayLike) -> Array:
  r"""Dirichlet log probability distribution function.

  JAX implementation of :obj:`scipy.stats.dirichlet` ``logpdf``.

  The Dirichlet probability density function is

  .. math::

     f(\mathbf{x}) = \frac{1}{B(\mathbf{\alpha})} \prod_{i=1}^K x_i^{\alpha_i - 1}

  where :math:`B(\mathbf{\alpha})` is the :func:`~jax.scipy.special.beta` function
  in a :math:`K`-dimensional vector space.

  Args:
    x: arraylike, value at which to evaluate the PDF
    alpha: arraylike, distribution shape parameter

  Returns:
    array of logpdf values.

  See Also:
    :func:`jax.scipy.stats.dirichlet.pdf`
  """
  return _logpdf(*promote_dtypes_inexact(x, alpha))


def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Exponential log probability distribution function.

  JAX implementation of :obj:`scipy.stats.expon` ``logpdf``.

  The Exponential probability distribution function is

  .. math::

     f(x) = \begin{cases}
       e^{-x} & x \ge 0 \\
       0 & \mathrm{otherwise}
     \end{cases}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    :func:`jax.scipy.stats.expon.cdf`
    :func:`jax.scipy.stats.expon.pdf`
    :func:`jax.scipy.stats.expon.ppf`
    :func:`jax.scipy.stats.expon.sf`
    :func:`jax.scipy.stats.expon.logcdf`
    :func:`jax.scipy.stats.expon.logpdf`
    :func:`jax.scipy.stats.expon.logsf`
  """
  x, loc, scale = promote_args_inexact("expon.logpdf", x, loc, scale)
  log_scale = lax.log(scale)
  linear_term = lax.div(lax.sub(x, loc), scale)
  log_probs = lax.neg(lax.add(linear_term, log_scale))
  return jnp.where(lax.lt(x, loc), -np.inf, log_probs)


def logpdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Gamma log probability distribution function.

  JAX implementation of :obj:`scipy.stats.gamma` ``logpdf``.

  The Gamma probability distribution is given by

  .. math::

     f(x, a) = \frac{1}{\Gamma(a)}x^{a-1}e^{-x}

  Where :math:`\Gamma(a)` is the :func:`~jax.scipy.special.gamma` function.
  It is defined for :math:`x \ge 0` and :math:`a > 0`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    a: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.gamma.cdf`
    - :func:`jax.scipy.stats.gamma.pdf`
    - :func:`jax.scipy.stats.gamma.sf`
    - :func:`jax.scipy.stats.gamma.logcdf`
    - :func:`jax.scipy.stats.gamma.logsf`
  """
  x, a, loc, scale = promote_args_inexact("gamma.logpdf", x, a, loc, scale)
  ok = lax.ge(x, loc)
  one = _lax_const(x, 1)
  y = jnp.where(ok, lax.div(lax.sub(x, loc), scale), one)
  log_linear_term = lax.sub(xlogy(lax.sub(a, one), y), y)
  shape_terms = lax.add(gammaln(a), lax.log(scale))
  log_probs = lax.sub(log_linear_term, shape_terms)
  return jnp.where(ok, log_probs, -np.inf)


def logpdf(x: ArrayLike, beta: ArrayLike) -> Array:
  r"""Generalized normal log probability distribution function.

  JAX implementation of :obj:`scipy.stats.gennorm` ``logpdf``.

  The generalized normal probability distribution function is defined as

  .. math::

     f(x, \beta) = \frac{\beta}{2\Gamma(1/\beta)}\exp(-|x|^\beta)

  where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function, and
  :math:`\beta > 0`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    beta: arraylike, distribution shape parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.gennorm.cdf`
    - :func:`jax.scipy.stats.gennorm.pdf`
  """
  x, beta = promote_args_inexact("gennorm.logpdf", x, beta)
  return lax.log(.5 * beta) - lax.lgamma(1/beta) - lax.abs(x)**beta


def logpdf(x: ArrayLike,
           loc: ArrayLike = 0,
           scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Left Skewed) log probability distribution function.

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``logpdf``.

   .. math::

      f_{pdf}(x; \mu, \beta) = \frac{1}{\beta} \exp\left( \frac{x - \mu}{\beta} - \exp\left( \frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate log(pdf)
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of logpdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_l.pdf`
    - :func:`jax.scipy.stats.gumbel_l.logcdf`
    - :func:`jax.scipy.stats.gumbel_l.cdf`
    - :func:`jax.scipy.stats.gumbel_l.ppf`
    - :func:`jax.scipy.stats.gumbel_l.logsf`
    - :func:`jax.scipy.stats.gumbel_l.sf`
  """

  x, loc, scale = promote_args_inexact("gumbel_l.logpdf", x, loc, scale)
  ok = lax.gt(scale, _lax_const(scale, 0))
  # logpdf = -log(scale) + z - exp(z)
  z = lax.div(lax.sub(x, loc), scale)
  neg_log_scale = xlogy(-1, scale)
  t2 = lax.sub(z, lax.exp(z))
  log_pdf = lax.add(neg_log_scale, t2)
  return jnp.where(ok, log_pdf, np.nan)


def logpdf(x: ArrayLike,
           loc: ArrayLike = 0,
           scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Right Skewed) log probability distribution function.

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``logpdf``.

  .. math::

      f_{pdf}(x; \mu, \beta) = \frac{1}{\beta} \exp\left( -\frac{x - \mu}{\beta} - \exp\left( -\frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate log(pdf)
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of logpdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_r.pdf`
    - :func:`jax.scipy.stats.gumbel_r.logcdf`
    - :func:`jax.scipy.stats.gumbel_r.cdf`
    - :func:`jax.scipy.stats.gumbel_r.ppf`
    - :func:`jax.scipy.stats.gumbel_r.sf`
    - :func:`jax.scipy.stats.gumbel_r.logsf`
  """

  x, loc, scale = promote_args_inexact("gumbel_r.logpdf", x, loc, scale)
  ok = lax.gt(scale, _lax_const(scale, 0))
  z = lax.div(lax.sub(x, loc), scale)
  # logpdf = -log(beta) - (z + exp(-z))
  neg_log_scale = xlogy(-1, scale)
  t2 = lax.neg(lax.add(z, lax.exp(lax.neg(z))))
  log_pdf = lax.add(neg_log_scale, t2)
  return jnp.where(ok, log_pdf, np.nan)


def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Laplace log probability distribution function.

  JAX implementation of :obj:`scipy.stats.laplace` ``logpdf``.

  The Laplace probability distribution function is given by

  .. math::

     f(x) = \frac{1}{2} e^{-|x|}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.laplace.cdf`
    - :func:`jax.scipy.stats.laplace.pdf`
  """
  x, loc, scale = promote_args_inexact("laplace.logpdf", x, loc, scale)
  two = _lax_const(x, 2)
  linear_term = lax.div(lax.abs(lax.sub(x, loc)), scale)
  return lax.neg(lax.add(linear_term, lax.log(lax.mul(two, scale))))


def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Logistic log probability distribution function.

  JAX implementation of :obj:`scipy.stats.logistic` ``logpdf``.

  The logistic probability distribution function is given by

  .. math::

     f(x) = \frac{e^{-x}}{(1 + e^{-x})^2}

  Args:
    x: arraylike, value at which to evaluate the PDF
    a: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.logistic.cdf`
    - :func:`jax.scipy.stats.logistic.pdf`
    - :func:`jax.scipy.stats.logistic.sf`
    - :func:`jax.scipy.stats.logistic.isf`
    - :func:`jax.scipy.stats.logistic.ppf`
  """
  x, loc, scale = promote_args_inexact("logistic.logpdf", x, loc, scale)
  x = lax.div(lax.sub(x, loc), scale)
  two = _lax_const(x, 2)
  half_x = lax.div(x, two)
  return lax.sub(lax.mul(lax.neg(two), jnp.logaddexp(half_x, lax.neg(half_x))), lax.log(scale))


def logpdf(x: ArrayLike, mean: ArrayLike, cov: ArrayLike, allow_singular: None = None) -> ArrayLike:
  r"""Multivariate normal log probability distribution function.

  JAX implementation of :obj:`scipy.stats.multivariate_normal` ``logpdf``.

  The multivariate normal PDF is defined as

  .. math::

     f(x) = \frac{1}{(2\pi)^k\det\Sigma}\exp\left(-\frac{(x-\mu)^T\Sigma^{-1}(x-\mu)}{2} \right)

  where :math:`\mu` is the ``mean``, :math:`\Sigma` is the covariance matrix (``cov``), and
  :math:`k` is the rank of :math:`\Sigma`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    mean: arraylike, centroid of distribution
    cov: arraylike, covariance matrix of distribution
    allow_singular: not supported

  Returns:
    array of logpdf values.

  See Also:
    :func:`jax.scipy.stats.multivariate_normal.pdf`
  """
  if allow_singular is not None:
    raise NotImplementedError("allow_singular argument of multivariate_normal.logpdf")
  x, mean, cov = promote_dtypes_inexact(x, mean, cov)
  if not mean.shape:
    return (-1/2 * jnp.square(x - mean) / cov
            - 1/2 * (jnp.log(2*np.pi) + jnp.log(cov)))
  else:
    n = mean.shape[-1]
    if not np.shape(cov):
      y = x - mean
      return (-1/2 * jnp_einsum.einsum('...i,...i->...', y, y) / cov
              - n/2 * (jnp.log(2*np.pi) + jnp.log(cov)))
    else:
      if cov.ndim < 2 or cov.shape[-2:] != (n, n):
        raise ValueError("multivariate_normal.logpdf got incompatible shapes")
      L = lax.linalg.cholesky(cov)
      y = jnp_vectorize.vectorize(
        partial(lax.linalg.triangular_solve, lower=True, transpose_a=True),
        signature="(n,n),(n)->(n)"
      )(L, x - mean)
      return (-1/2 * jnp_einsum.einsum('...i,...i->...', y, y) - n/2 * jnp.log(2*np.pi)
              - jnp.log(L.diagonal(axis1=-1, axis2=-2)).sum(-1))


def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Normal log probability distribution function.

  JAX implementation of :obj:`scipy.stats.norm` ``logpdf``.

  The normal distribution pdf is given by

  .. math::

     f(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.norm.cdf`
    - :func:`jax.scipy.stats.norm.pdf`
    - :func:`jax.scipy.stats.norm.sf`
    - :func:`jax.scipy.stats.norm.logcdf`
    - :func:`jax.scipy.stats.norm.logsf`
    - :func:`jax.scipy.stats.norm.isf`
    - :func:`jax.scipy.stats.norm.ppf`
  """
  x, loc, scale = promote_args_inexact("norm.logpdf", x, loc, scale)
  scale_sqrd = lax.square(scale)
  log_normalizer = lax.log(lax.mul(_lax_const(x, 2 * np.pi), scale_sqrd))
  quadratic = lax.div(lax.square(lax.sub(x, loc)), scale_sqrd)
  return lax.div(lax.add(log_normalizer, quadratic), _lax_const(x, -2))


def logpdf(
  x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1
) -> Array:
  r"""Pareto log probability distribution function.

  JAX implementation of :obj:`scipy.stats.pareto` ``logpdf``.

  The Pareto probability density function is given by

  .. math::

     f(x, b) = \begin{cases}
       bx^{-(b+1)} & x \ge 1\\
       0 & x < 1
     \end{cases}

  and is defined for :math:`b > 0`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.pareto.logcdf`
    - :func:`jax.scipy.stats.pareto.logsf`
    - :func:`jax.scipy.stats.pareto.cdf`
    - :func:`jax.scipy.stats.pareto.pdf`
    - :func:`jax.scipy.stats.pareto.ppf`
    - :func:`jax.scipy.stats.pareto.sf`
  """
  x, b, loc, scale = promote_args_inexact("pareto.logpdf", x, b, loc, scale)
  one = _lax_const(x, 1)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  normalize_term = lax.log(lax.div(scale, b))
  log_probs = lax.neg(
    lax.add(normalize_term, lax.mul(lax.add(b, one), lax.log(scaled_x)))
  )
  return jnp.where(lax.lt(x, lax.add(loc, scale)), -np.inf, log_probs)


def logpdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Student's T log probability distribution function.

  JAX implementation of :obj:`scipy.stats.t` ``logpdf``.

  The Student's T probability distribution function is given by

  .. math::

     f(x, \nu) = \frac{\Gamma((\nu + 1)/2)}{\sqrt{\pi\nu}\Gamma(\nu/2)}(1 + x^2/\nu)^{(\nu+1)/2}

  Where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function, and :math:`\nu > 0`
  is the degrees of freedom (JAX follows the scipy convention of naming this ``df``).

  Args:
    x: arraylike, value at which to evaluate the PDF
    df: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    :func:`jax.scipy.stats.t.pdf`
  """
  x, df, loc, scale = promote_args_inexact("t.logpdf", x, df, loc, scale)
  two = _lax_const(x, 2)
  scaled_x = lax.div(lax.sub(x, loc), scale)
  df_over_two = lax.div(df, two)
  df_plus_one_over_two = lax.add(df_over_two, _lax_const(x, 0.5))
  normalize_term_const = lax.mul(lax.mul(scale, scale), _lax_const(x, np.pi))
  normalize_term_tmp = lax.div(lax.log(lax.mul(normalize_term_const, df)), two)
  normalize_term = lax.sub(lax.add(lax.lgamma(df_over_two), normalize_term_tmp),
                           lax.lgamma(df_plus_one_over_two))
  quadratic = lax.div(lax.mul(scaled_x, scaled_x), df)
  return lax.neg(lax.add(normalize_term, lax.mul(df_plus_one_over_two, lax.log1p(quadratic))))


def logpdf(x, a, b, loc=0, scale=1):
  r"""Truncated normal log probability distribution function.

  JAX implementation of :obj:`scipy.stats.truncnorm` ``logpdf``.

  The truncated normal probability distribution is given by

  .. math::

     f(x, a, b) = \begin{cases}
       \frac{1}{\sqrt{2\pi}}e^{-x^2/2} & a \le x \le b \\
       0 & \mathrm{otherwise}
     \end{cases}

  where :math:`a` and :math:`b` are effectively specified in number of
  standard deviations from zero. JAX uses the scipy nomenclature
  of ``loc`` for the centroid and ``scale`` for the standard deviation.

  Args:
    x: arraylike, value at which to evaluate the PDF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values.

  See Also:
    - :func:`jax.scipy.stats.truncnorm.cdf`
    - :func:`jax.scipy.stats.truncnorm.pdf`
    - :func:`jax.scipy.stats.truncnorm.sf`
    - :func:`jax.scipy.stats.truncnorm.logcdf`
    - :func:`jax.scipy.stats.truncnorm.logsf`
  """
  x, a, b, loc, scale = promote_args_inexact("truncnorm.logpdf", x, a, b, loc, scale)
  val = lax.sub(norm.logpdf(x, loc, scale), _log_gauss_mass(a, b))

  x_scaled = lax.div(lax.sub(x, loc), scale)
  val = jnp.where((x_scaled < a) | (x_scaled > b), -np.inf, val)
  val = jnp.where(a >= b, np.nan, val)
  return val


def logpdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Uniform log probability distribution function.

  JAX implementation of :obj:`scipy.stats.uniform` ``logpdf``.

  The uniform distribution pdf is given by

  .. math::

     f(x) = \begin{cases}
       1 & 0 \le x \le 1 \\
       0 & \mathrm{otherwise}
     \end{cases}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of logpdf values

  See Also:
    - :func:`jax.scipy.stats.uniform.cdf`
    - :func:`jax.scipy.stats.uniform.pdf`
    - :func:`jax.scipy.stats.uniform.ppf`
  """
  x, loc, scale = promote_args_inexact("uniform.logpdf", x, loc, scale)
  log_probs = lax.neg(lax.log(scale))
  return jnp.where(jnp.logical_or(lax.gt(x, lax.add(loc, scale)),
                                  lax.lt(x, loc)),
                   -np.inf, log_probs)


def logpdf(x: ArrayLike, kappa: ArrayLike) -> Array:
  r"""von Mises log probability distribution function.

  JAX implementation of :obj:`scipy.stats.vonmises` ``logpdf``.

  The von Mises probability distribution function is given by

  .. math::

     f(x, \kappa) = \frac{1}{2\pi I_0(\kappa)}e^{\kappa\cos x}

  Where :math:`I_0` is the modified Bessel function :func:`~jax.scipy.special.i0`
  and :math:`\kappa\ge 0`, and the distribution is normalized in the interval
  :math:`-\pi \le x \le \pi`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    kappa: arraylike, distribution shape parameter

  Returns:
    array of logpdf values.

  See Also:
    :func:`jax.scipy.stats.vonmises.pdf`
  """
  x, kappa = promote_args_inexact('vonmises.logpdf', x, kappa)
  zero = _lax_const(kappa, 0)
  return jnp.where(lax.gt(kappa, zero), kappa * (jnp.cos(x) - 1) - jnp.log(2 * np.pi * lax.bessel_i0e(kappa)), np.nan)


def logpdf(x: ArrayLike, c: ArrayLike) -> Array:
  r"""Wrapped Cauchy log probability distribution function.

  JAX implementation of :obj:`scipy.stats.wrapcauchy` ``logpdf``.

  The wrapped Cauchy probability distribution function is given by

  .. math::

     f(x, c) = \frac{1-c^2}{2\pi(1+c^2-2c\cos x)}

  for :math:`0<c<1`, and where normalization is on the domain :math:`0\le x\le 2\pi`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    c: arraylike, distribution shape parameter

  Returns:
    array of logpdf values.

  See Also:
    :func:`jax.scipy.stats.wrapcauchy.pdf`
  """
  x, c = promote_args_inexact('wrapcauchy.logpdf', x, c)
  return jnp.where(
    lax.gt(c, _lax_const(c, 0)) & lax.lt(c, _lax_const(c, 1)),
    jnp.where(
      lax.ge(x, _lax_const(x, 0)) & lax.le(x, _lax_const(x, np.pi * 2)),
      jnp.log(1 - c * c) - jnp.log(2 * np.pi) - jnp.log(1 + c * c - 2 * c * jnp.cos(x)),
      -np.inf,
    ),
    np.nan,
  )

