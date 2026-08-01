
def pdf(x: ArrayLike, a: ArrayLike, b: ArrayLike,
        loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Beta probability distribution function.

  JAX implementation of :obj:`scipy.stats.beta` ``pdf``.

  The pdf of the beta function is:

  .. math::

    f(x, a, b) = \frac{\Gamma(a + b)}{\Gamma(a)\Gamma(b)} x^{a-1}(1-x)^{b-1}

  where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function.
  It is defined for :math:`0\le x\le 1` and :math:`b>0`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of pdf values

  See Also:
    - :func:`jax.scipy.stats.beta.cdf`
    - :func:`jax.scipy.stats.beta.sf`
    - :func:`jax.scipy.stats.beta.logcdf`
    - :func:`jax.scipy.stats.beta.logpdf`
    - :func:`jax.scipy.stats.beta.logsf`
  """
  return lax.exp(logpdf(x, a, b, loc, scale))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Cauchy probability distribution function.

  JAX implementation of :obj:`scipy.stats.cauchy` ``pdf``.

  The Cauchy probability distribution function is

  .. math::

     f(x) = \frac{1}{\pi(1 + x^2)}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of pdf values

  See Also:
    - :func:`jax.scipy.stats.cauchy.cdf`
    - :func:`jax.scipy.stats.cauchy.sf`
    - :func:`jax.scipy.stats.cauchy.logcdf`
    - :func:`jax.scipy.stats.cauchy.logpdf`
    - :func:`jax.scipy.stats.cauchy.logsf`
    - :func:`jax.scipy.stats.cauchy.isf`
    - :func:`jax.scipy.stats.cauchy.ppf`
  """
  return lax.exp(logpdf(x, loc, scale))


def pdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Chi-square probability distribution function.

  JAX implementation of :obj:`scipy.stats.chi2` ``pdf``.

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
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.chi2.cdf`
    - :func:`jax.scipy.stats.chi2.sf`
    - :func:`jax.scipy.stats.chi2.logcdf`
    - :func:`jax.scipy.stats.chi2.logpdf`
    - :func:`jax.scipy.stats.chi2.logsf`
  """
  return lax.exp(logpdf(x, df, loc, scale))


def pdf(x: ArrayLike, alpha: ArrayLike) -> Array:
  r"""Dirichlet probability distribution function.

  JAX implementation of :obj:`scipy.stats.dirichlet` ``pdf``.

  The Dirichlet probability density function is

  .. math::

     f(\mathbf{x}) = \frac{1}{B(\mathbf{\alpha})} \prod_{i=1}^K x_i^{\alpha_i - 1}

  where :math:`B(\mathbf{\alpha})` is the :func:`~jax.scipy.special.beta` function
  in a :math:`K`-dimensional vector space.

  Args:
    x: arraylike, value at which to evaluate the PDF
    alpha: arraylike, distribution shape parameter

  Returns:
    array of pdf values.

  See Also:
    :func:`jax.scipy.stats.dirichlet.logpdf`
  """
  return lax.exp(logpdf(x, alpha))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Exponential probability distribution function.

  JAX implementation of :obj:`scipy.stats.expon` ``pdf``.

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
  return lax.exp(logpdf(x, loc, scale))


def pdf(x: ArrayLike, a: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Gamma probability distribution function.

  JAX implementation of :obj:`scipy.stats.gamma` ``pdf``.

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
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.gamma.cdf`
    - :func:`jax.scipy.stats.gamma.sf`
    - :func:`jax.scipy.stats.gamma.logcdf`
    - :func:`jax.scipy.stats.gamma.logpdf`
    - :func:`jax.scipy.stats.gamma.logsf`
  """
  return lax.exp(logpdf(x, a, loc, scale))


def pdf(x: ArrayLike, beta: ArrayLike) -> Array:
  r"""Generalized normal probability distribution function.

  JAX implementation of :obj:`scipy.stats.gennorm` ``pdf``.

  The generalized normal probability distribution function is defined as

  .. math::

     f(x, \beta) = \frac{\beta}{2\Gamma(1/\beta)}\exp(-|x|^\beta)

  where :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function, and
  :math:`\beta > 0`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    beta: arraylike, distribution shape parameter

  Returns:
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.gennorm.cdf`
    - :func:`jax.scipy.stats.gennorm.logpdf`
  """
  return lax.exp(logpdf(x, beta))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Left Skewed) probability distribution function.

  JAX implementation of :obj:`scipy.stats.gumbel_l` ``pdf``.

  .. math::

      f_{pdf}(x; \mu, \beta) = \frac{1}{\beta} \exp\left( \frac{x - \mu}{\beta} - \exp\left( \frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate pdf
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of pdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_l.logpdf`
    - :func:`jax.scipy.stats.gumbel_l.logcdf`
    - :func:`jax.scipy.stats.gumbel_l.cdf`
    - :func:`jax.scipy.stats.gumbel_l.ppf`
    - :func:`jax.scipy.stats.gumbel_l.logsf`
    - :func:`jax.scipy.stats.gumbel_l.sf`
  """
  return lax.exp(logpdf(x, loc, scale))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""
  Gumbel Distribution (Right Skewed) probability distribution function.

  JAX implementation of :obj:`scipy.stats.gumbel_r` ``pdf``.

  .. math::

      f_{pdf}(x; \mu, \beta) = \frac{1}{\beta} \exp\left( -\frac{x - \mu}{\beta} - \exp\left( -\frac{x - \mu}{\beta} \right) \right)

  Args:
    x: ArrayLike, value at which to evaluate pdf
    loc: ArrayLike, distribution offset (:math:`\mu`) (defaulted to 0)
    scale: ArrayLike, distribution scaling (:math:`\beta`) (defaulted to 1)

  Returns:
    array of pdf values

  See Also:
    - :func:`jax.scipy.stats.gumbel_r.logpdf`
    - :func:`jax.scipy.stats.gumbel_r.logcdf`
    - :func:`jax.scipy.stats.gumbel_r.cdf`
    - :func:`jax.scipy.stats.gumbel_r.ppf`
    - :func:`jax.scipy.stats.gumbel_r.sf`
    - :func:`jax.scipy.stats.gumbel_r.logsf`
  """
  return lax.exp(logpdf(x, loc, scale))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Laplace probability distribution function.

  JAX implementation of :obj:`scipy.stats.laplace` ``pdf``.

  The Laplace probability distribution function is given by

  .. math::

     f(x) = \frac{1}{2} e^{-|x|}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.laplace.cdf`
    - :func:`jax.scipy.stats.laplace.logpdf`
  """
  return lax.exp(logpdf(x, loc, scale))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Logistic probability distribution function.

  JAX implementation of :obj:`scipy.stats.logistic` ``pdf``.

  The logistic probability distribution function is given by

  .. math::

     f(x) = \frac{e^{-x}}{(1 + e^{-x})^2}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.logistic.cdf`
    - :func:`jax.scipy.stats.logistic.sf`
    - :func:`jax.scipy.stats.logistic.isf`
    - :func:`jax.scipy.stats.logistic.logpdf`
    - :func:`jax.scipy.stats.logistic.ppf`
  """
  return lax.exp(logpdf(x, loc, scale))


def pdf(x: ArrayLike, mean: ArrayLike, cov: ArrayLike) -> Array:
  r"""Multivariate normal probability distribution function.

  JAX implementation of :obj:`scipy.stats.multivariate_normal` ``pdf``.

  The multivariate normal PDF is defined as

  .. math::

     f(x) = \frac{1}{(2\pi)^k\det\Sigma}\exp\left(-\frac{(x-\mu)^T\Sigma^{-1}(x-\mu)}{2} \right)

  where :math:`\mu` is the ``mean``, :math:`\Sigma` is the covariance matrix (``cov``), and
  :math:`k` is the rank of :math:`\Sigma`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    mean: arraylike, centroid of distribution
    cov: arraylike, covariance matrix of distribution

  Returns:
    array of pdf values.

  See Also:
    :func:`jax.scipy.stats.multivariate_normal.logpdf`
  """
  return lax.exp(logpdf(x, mean, cov))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Normal probability distribution function.

  JAX implementation of :obj:`scipy.stats.norm` ``pdf``.

  The normal distribution pdf is given by

  .. math::

     f(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}

  Args:
    x: arraylike, value at which to evaluate the PDF
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.norm.cdf`
    - :func:`jax.scipy.stats.norm.sf`
    - :func:`jax.scipy.stats.norm.logcdf`
    - :func:`jax.scipy.stats.norm.logpdf`
    - :func:`jax.scipy.stats.norm.logsf`
    - :func:`jax.scipy.stats.norm.isf`
    - :func:`jax.scipy.stats.norm.ppf`
  """
  return lax.exp(logpdf(x, loc, scale))


def pdf(
  x: ArrayLike, b: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1
) -> Array:
  r"""Pareto probability distribution function.

  JAX implementation of :obj:`scipy.stats.pareto` ``pdf``.

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
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.pareto.logcdf`
    - :func:`jax.scipy.stats.pareto.logpdf`
    - :func:`jax.scipy.stats.pareto.logsf`
    - :func:`jax.scipy.stats.pareto.cdf`
    - :func:`jax.scipy.stats.pareto.ppf`
    - :func:`jax.scipy.stats.pareto.sf`
  """
  return lax.exp(logpdf(x, b, loc, scale))


def pdf(x: ArrayLike, df: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Student's T probability distribution function.

  JAX implementation of :obj:`scipy.stats.t` ``pdf``.

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
    array

  See Also:
    :func:`jax.scipy.stats.t.logpdf`
  """
  return lax.exp(logpdf(x, df, loc, scale))


def pdf(x, a, b, loc=0, scale=1):
  r"""Truncated normal probability distribution function.

  JAX implementation of :obj:`scipy.stats.truncnorm` ``pdf``.

  The truncated normal probability distribution is given by

  .. math::

     f(x, a, b) = \begin{cases}
       \frac{1}{\sqrt{2\pi}}e^{-x^2/2} & a \le x \le b \\
       0 & \mathrm{otherwise}
     \end{cases}

  where :math:`a` and :math:`b` are effectively specified in number of
  standard deviations from the centroid. JAX uses the scipy nomenclature
  of ``loc`` for the centroid and ``scale`` for the standard deviation.

  Args:
    x: arraylike, value at which to evaluate the PDF
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter
    scale: arraylike, distribution scale parameter

  Returns:
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.truncnorm.cdf`
    - :func:`jax.scipy.stats.truncnorm.sf`
    - :func:`jax.scipy.stats.truncnorm.logcdf`
    - :func:`jax.scipy.stats.truncnorm.logpdf`
    - :func:`jax.scipy.stats.truncnorm.logsf`
  """
  return lax.exp(logpdf(x, a, b, loc, scale))


def pdf(x: ArrayLike, loc: ArrayLike = 0, scale: ArrayLike = 1) -> Array:
  r"""Uniform probability distribution function.

  JAX implementation of :obj:`scipy.stats.uniform` ``pdf``.

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
    array of pdf values.

  See Also:
    - :func:`jax.scipy.stats.uniform.cdf`
    - :func:`jax.scipy.stats.uniform.logpdf`
    - :func:`jax.scipy.stats.uniform.ppf`
  """
  return lax.exp(logpdf(x, loc, scale))


def pdf(x: ArrayLike, kappa: ArrayLike) -> Array:
  r"""von Mises probability distribution function.

  JAX implementation of :obj:`scipy.stats.vonmises` ``pdf``.

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
    array of pdf values.

  See Also:
    :func:`jax.scipy.stats.vonmises.logpdf`
  """
  return lax.exp(logpdf(x, kappa))


def pdf(x: ArrayLike, c: ArrayLike) -> Array:
  r"""Wrapped Cauchy probability distribution function.

  JAX implementation of :obj:`scipy.stats.wrapcauchy` ``pdf``.

  The wrapped Cauchy probability distribution function is given by

  .. math::

     f(x, c) = \frac{1-c^2}{2\pi(1+c^2-2c\cos x)}

  for :math:`0<c<1`, and where normalization is on the domain :math:`0\le x\le 2\pi`.

  Args:
    x: arraylike, value at which to evaluate the PDF
    c: arraylike, distribution shape parameter

  Returns:
    array of pdf values.

  See Also:
    :func:`jax.scipy.stats.wrapcauchy.logpdf`
  """
  return lax.exp(logpdf(x, c))

