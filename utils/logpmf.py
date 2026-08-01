
def logpmf(k: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Bernoulli log probability mass function.

  JAX implementation of :obj:`scipy.stats.bernoulli` ``logpmf``

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
    array of logpmf values

  See Also:
    - :func:`jax.scipy.stats.bernoulli.cdf`
    - :func:`jax.scipy.stats.bernoulli.pmf`
    - :func:`jax.scipy.stats.bernoulli.ppf`
  """
  k, p, loc = promote_args_inexact("bernoulli.logpmf", k, p, loc)
  zero = _lax_const(k, 0)
  one = _lax_const(k, 1)
  x = lax.sub(k, loc)
  log_probs = xlogy(x, p) + xlog1py(lax.sub(one, x), -p)
  return jnp.where(jnp.logical_or(lax.lt(x, zero), lax.gt(x, one)),
                  -np.inf, log_probs)


def logpmf(k: ArrayLike, n: ArrayLike, a: ArrayLike, b: ArrayLike,
           loc: ArrayLike = 0) -> Array:
  r"""Beta-binomial log probability mass function.

  JAX implementation of :obj:`scipy.stats.betabinom` ``logpmf``

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
    array of logpmf values

  See Also:
    :func:`jax.scipy.stats.betabinom.pmf`
  """
  k, n, a, b, loc = promote_args_inexact("betabinom.logpmf", k, n, a, b, loc)
  y = lax.sub(lax.floor(k), loc)
  one = _lax_const(y, 1)
  zero = _lax_const(y, 0)
  combiln = lax.neg(lax.add(lax.log1p(n), betaln(lax.add(lax.sub(n,y), one), lax.add(y,one))))
  beta_lns = lax.sub(betaln(lax.add(y,a), lax.add(lax.sub(n,y),b)), betaln(a,b))
  log_probs = lax.add(combiln, beta_lns)
  log_probs = jnp.where(jnp.logical_and(lax.eq(y, zero), lax.eq(n, zero)), 0., log_probs)
  y_cond = jnp.logical_or(jnp.logical_or(lax.lt(y, lax.neg(loc)), lax.gt(y, n)),
                          lax.le(lax.add(y, a), zero))
  log_probs = jnp.where(y_cond, -np.inf, log_probs)
  n_a_b_cond = jnp.logical_or(jnp.logical_or(lax.lt(n, zero), lax.le(a, zero)), lax.le(b, zero))
  return jnp.where(n_a_b_cond, np.nan, log_probs)


def logpmf(k: ArrayLike, n: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Binomial log probability mass function.

  JAX implementation of :obj:`scipy.stats.binom` ``logpmf``.

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
    array of logpmf values.

  See Also:
    :func:`jax.scipy.stats.binom.pmf`
  """
  k, n, p, loc = promote_args_inexact("binom.logpmf", k, n, p, loc)
  y = lax.sub(k, loc)
  zero = _lax_const(y, 0)
  comb_term = lax.sub(
      gammaln(n + 1),
      lax.add(gammaln(y + 1), gammaln(n - y + 1))
  )
  log_linear_term = lax.add(xlogy(y, p), xlog1py(lax.sub(n, y), lax.neg(p)))
  log_probs = lax.add(comb_term, log_linear_term)
  y_n_cond = jnp.logical_or(jnp.logical_and(lax.eq(y, zero), lax.eq(n, zero)),
                            lax.eq(log_linear_term, zero))
  log_probs = jnp.where(y_n_cond, 0., log_probs)
  return jnp.where(lax.ge(k, loc) & lax.lt(k, loc + n + 1), log_probs, -np.inf)


def logpmf(k: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Geometric log probability mass function.

  JAX implementation of :obj:`scipy.stats.geom` ``logpmf``.

  The Geometric probability mass function is given by

  .. math::

     f(k) = (1 - p)^{k-1}p

  for :math:`k\ge 1` and :math:`0 \le p \le 1`.

  Args:
    k: arraylike, value at which to evaluate the PMF
    p: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
    array of logpmf values.

  See Also:
    :func:`jax.scipy.stats.geom.pmf`
  """
  k, p, loc = promote_args_inexact("geom.logpmf", k, p, loc)
  zero = _lax_const(k, 0)
  one = _lax_const(k, 1)
  x = lax.sub(k, loc)
  log_probs = xlog1py(lax.sub(x, one), -p) + lax.log(p)
  return jnp.where(lax.le(x, zero), -np.inf, log_probs)


def logpmf(x: ArrayLike, n: ArrayLike, p: ArrayLike) -> Array:
  r"""Multinomial log probability mass function.

  JAX implementation of :obj:`scipy.stats.multinomial` ``logpdf``.

  The multinomial probability distribution is given by

  .. math::

     f(x, n, p) = n! \prod_{i=1}^k \frac{p_i^{x_i}}{x_i!}

  with :math:`n = \sum_i x_i`.

  Args:
    x: arraylike, value at which to evaluate the PMF
    n: arraylike, distribution shape parameter
    p: arraylike, distribution shape parameter

  Returns:
    array of logpmf values.

  See Also:
    :func:`jax.scipy.stats.multinomial.pmf`
  """
  p, = promote_args_inexact("multinomial.logpmf", p)
  x, n = promote_args_numeric("multinomial.logpmf", x, n)
  if not dtypes.issubdtype(x.dtype, np.integer):
    raise ValueError(f"x and n must be of integer type; got x.dtype={x.dtype}, n.dtype={n.dtype}")
  x = x.astype(p.dtype)
  n = n.astype(p.dtype)
  logprobs = gammaln(n + 1) + jnp.sum(xlogy(x, p) - gammaln(x + 1), axis=-1)
  return jnp.where(jnp.equal(jnp.sum(x), n), logprobs, -np.inf)


def logpmf(k: ArrayLike, n: ArrayLike, p: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Negative-binomial log probability mass function.

  JAX implementation of :obj:`scipy.stats.nbinom` ``logpmf``.

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
    array of logpmf values.

  See Also:
    :func:`jax.scipy.stats.nbinom.pmf`
  """
  k, n, p, loc = promote_args_inexact("nbinom.logpmf", k, n, p, loc)
  one = _lax_const(k, 1)
  y = lax.sub(k, loc)
  comb_term = lax.sub(
    lax.sub(gammaln(lax.add(y, n)), gammaln(n)), gammaln(lax.add(y, one))
  )
  log_linear_term = lax.add(xlogy(n, p), xlogy(y, lax.sub(one, p)))
  log_probs = lax.add(comb_term, log_linear_term)
  return jnp.where(lax.lt(k, loc), -np.inf, log_probs)


def logpmf(k: ArrayLike, mu: ArrayLike, loc: ArrayLike = 0) -> Array:
  r"""Poisson log probability mass function.

  JAX implementation of :obj:`scipy.stats.poisson` ``logpmf``.

  The Poisson probability mass function is given by

  .. math::

     f(k) = e^{-\mu}\frac{\mu^k}{k!}

  and is defined for :math:`k \ge 0` and :math:`\mu \ge 0`.

  Args:
    k: arraylike, value at which to evaluate the PMF
    mu: arraylike, distribution shape parameter
    loc: arraylike, distribution offset parameter

  Returns:
    array of logpmf values.

  See Also:
    - :func:`jax.scipy.stats.poisson.cdf`
    - :func:`jax.scipy.stats.poisson.pmf`
    - :func:`jax.scipy.stats.poisson.entropy`
  """
  k, mu, loc = promote_args_inexact("poisson.logpmf", k, mu, loc)
  zero = _lax_const(k, 0)
  x = lax.sub(k, loc)
  log_probs = xlogy(x, mu) - gammaln(x + 1) - mu
  return jnp.where(jnp.logical_or(lax.lt(x, zero),
                                  lax.ne(jnp.round(k), k)), -np.inf, log_probs)

