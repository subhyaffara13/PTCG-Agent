
def pmf(k: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Bernoulli probability mass function.

  JAX implementation of :obj:`scipy.stats.bernoulli` ``pmf``

  The Bernoulli probability mass function is defined as

  .. math::

     f(k) = \begin{cases}
       1 - p, & k = 0 \\
       p, & k = 1 \\
       0, & \mathrm{otherwise}
     \end{cases}

  Args:
    k: arraylike, value at which to evaluate the PMF
    p: arraylike, distribution shape parameter
    loc: arraylike, distribution offset

  Returns:
    array of pmf values

  See Also:
    - :func:`jax.scipy.stats.bernoulli.cdf`
    - :func:`jax.scipy.stats.bernoulli.logpmf`
    - :func:`jax.scipy.stats.bernoulli.ppf`
  """
  return jnp.exp(logpmf(k, p, loc))


def pmf(k: ArrayLike, n: ArrayLike, a: ArrayLike, b: ArrayLike,
        loc: ArrayLike = 0) -> Array:
  r"""Beta-binomial probability mass function.

  JAX implementation of :obj:`scipy.stats.betabinom` ``pmf``.

  The beta-binomial distribution's probability mass function is defined as

  .. math::

     f(k, n, a, b) = {n \choose k}\frac{B(k+a,n-k+b)}{B(a,b)}

  where :math:`B(a, b)` is the :func:`~jax.scipy.special.beta` function. It is
  defined for :math:`n\ge 0`, :math:`a>0`, :math:`b>0`, and non-negative integers `k`.

  Args:
    k: arraylike, value at which to evaluate the PMF
    n: arraylike, distribution shape parameter
    a: arraylike, distribution shape parameter
    b: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
    array of pmf values

  See Also:
    :func:`jax.scipy.stats.betabinom.logpmf`
  """
  return lax.exp(logpmf(k, n, a, b, loc))


def pmf(k: ArrayLike, n: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Binomial probability mass function.

  JAX implementation of :obj:`scipy.stats.binom` ``pmf``.

  The binomial probability mass function is defined as

  .. math::

     f(k, n, p) = {n \choose k}p^k(1-p)^{n-k}

  for :math:`0\le p\le 1` and non-negative integers :math:`k`.

  Args:
    k: arraylike, value at which to evaluate the PMF
    n: arraylike, distribution shape parameter
    p: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
      array of pmf values.

  See Also:
    :func:`jax.scipy.stats.binom.logpmf`
  """
  return lax.exp(logpmf(k, n, p, loc))


def pmf(k: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Geometric probability mass function.

  JAX implementation of :obj:`scipy.stats.geom` ``pmf``.

  The Geometric probability mass function is given by

  .. math::

     f(k) = (1 - p)^{k-1}p

  for :math:`k\ge 1` and :math:`0 \le p \le 1`.

  Args:
    k: arraylike, value at which to evaluate the PMF
    p: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
    array of pmf values.

  See Also:
    :func:`jax.scipy.stats.geom.logpmf`
  """
  return jnp.exp(logpmf(k, p, loc))


def pmf(x: ArrayLike, n: ArrayLike, p: ArrayLike) -> Array:
  r"""Multinomial probability mass function.

  JAX implementation of :obj:`scipy.stats.multinomial` ``pmf``.

  The multinomial probability distribution is given by

  .. math::

     f(x, n, p) = n! \prod_{i=1}^k \frac{p_i^{x_i}}{x_i!}

  with :math:`n = \sum_i x_i`.

  Args:
    x: arraylike, value at which to evaluate the PMF
    n: arraylike, distribution shape parameter
    p: arraylike, distribution shape parameter

  Returns:
    array of pmf values

  See Also:
    :func:`jax.scipy.stats.multinomial.logpmf`
  """
  return lax.exp(logpmf(x, n, p))


def pmf(k: ArrayLike, n: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Negative-binomial probability mass function.

  JAX implementation of :obj:`scipy.stats.nbinom` ``pmf``.

  The negative-binomial probability mass function is given by

  .. math::

     f(k) = {{k+n-1} \choose {n-1}}p^n(1-p)^k

  for :math:`k \ge 0` and :math:`0 \le p \le 1`.

  Args:
    k: arraylike, value at which to evaluate the PMF
    n: arraylike, distribution shape parameter
    p: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
    array of pmf values.

  See Also:
    :func:`jax.scipy.stats.nbinom.logpmf`
  """
  return lax.exp(logpmf(k, n, p, loc))


def pmf(k: ArrayLike, mu: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Poisson probability mass function.

  JAX implementation of :obj:`scipy.stats.poisson` ``pmf``.

  The Poisson probability mass function is given by

  .. math::

     f(k) = e^{-\mu}\frac{\mu^k}{k!}

  and is defined for :math:`k \ge 0` and :math:`\mu \ge 0`.

  Args:
    k: arraylike, value at which to evaluate the PMF
    mu: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
    array of pmf values.

  See Also:
    - :func:`jax.scipy.stats.poisson.cdf`
    - :func:`jax.scipy.stats.poisson.logpmf`
    - :func:`jax.scipy.stats.poisson.entropy`
  """
  return jnp.exp(logpmf(k, mu, loc))

