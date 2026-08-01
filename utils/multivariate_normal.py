
def MultivariateNormal(name, mu, sigma):
    r"""
    Creates a continuous random variable with Multivariate Normal
    Distribution.

    The density of the multivariate normal distribution can be found at [1].

    Parameters
    ==========

    mu : List representing the mean or the mean vector
    sigma : Positive semidefinite square matrix
        Represents covariance Matrix.
        If `\sigma` is noninvertible then only sampling is supported currently

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import MultivariateNormal, density, marginal_distribution
    >>> from sympy import symbols, MatrixSymbol
    >>> X = MultivariateNormal('X', [3, 4], [[2, 1], [1, 2]])
    >>> y, z = symbols('y z')
    >>> density(X)(y, z)
    sqrt(3)*exp(-y**2/3 + y*z/3 + 2*y/3 - z**2/3 + 5*z/3 - 13/3)/(6*pi)
    >>> density(X)(1, 2)
    sqrt(3)*exp(-4/3)/(6*pi)
    >>> marginal_distribution(X, X[1])(y)
    exp(-(y - 4)**2/4)/(2*sqrt(pi))
    >>> marginal_distribution(X, X[0])(y)
    exp(-(y - 3)**2/4)/(2*sqrt(pi))

    The example below shows that it is also possible to use
    symbolic parameters to define the MultivariateNormal class.

    >>> n = symbols('n', integer=True, positive=True)
    >>> Sg = MatrixSymbol('Sg', n, n)
    >>> mu = MatrixSymbol('mu', n, 1)
    >>> obs = MatrixSymbol('obs', n, 1)
    >>> X = MultivariateNormal('X', mu, Sg)

    The density of a multivariate normal can be
    calculated using a matrix argument, as shown below.

    >>> density(X)(obs)
    (exp(((1/2)*mu.T - (1/2)*obs.T)*Sg**(-1)*(-mu + obs))/sqrt((2*pi)**n*Determinant(Sg)))[0, 0]

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Multivariate_normal_distribution

    """
    return multivariate_rv(MultivariateNormalDistribution, name, mu, sigma)


def multivariate_normal(key: ArrayLike,
                        mean: RealArray,
                        cov: RealArray,
                        shape: Shape | None = None,
                        dtype: DTypeLikeFloat | None = None,
                        method: str = 'cholesky',
                        *,
                        out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample multivariate normal random values with given mean and covariance.

  The values are returned according to the probability density function:

  .. math::
     f(x;\mu, \Sigma) = (2\pi)^{-k/2} \det(\Sigma)^{-1}e^{-\frac{1}{2}(x - \mu)^T \Sigma^{-1} (x - \mu)}

  where :math:`k` is the dimension, :math:`\mu` is the mean (given by ``mean``) and
  :math:`\Sigma` is the covariance matrix (given by ``cov``).

  Args:
    key: a PRNG key used as the random key.
    mean: a mean vector of shape ``(..., n)``.
    cov: a positive definite covariance matrix of shape ``(..., n, n)``. The
      batch shape ``...`` must be broadcast-compatible with that of ``mean``.
    shape: optional, a tuple of nonnegative integers specifying the result
      batch shape; that is, the prefix of the result shape excluding the last
      axis. Must be broadcast-compatible with ``mean.shape[:-1]`` and
      ``cov.shape[:-2]``. The default (None) produces a result batch shape by
      broadcasting together the batch shapes of ``mean`` and ``cov``.
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    method: optional, a method to compute the factor of ``cov``.
      Must be one of 'svd', 'eigh', and 'cholesky'. Default 'cholesky'. For
      singular covariance matrices, use 'svd' or 'eigh'.
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified dtype and shape given by
    ``shape + mean.shape[-1:]`` if ``shape`` is not None, or else
    ``broadcast_shapes(mean.shape[:-1], cov.shape[:-2]) + mean.shape[-1:]``.
  """
  key, _ = _check_prng_key("multivariate_normal", key)
  mean, cov = promote_dtypes_inexact(mean, cov)
  if method not in {'svd', 'eigh', 'cholesky'}:
    raise ValueError("method must be one of {'svd', 'eigh', 'cholesky'}")
  if dtype is None:
    dtype = mean.dtype
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `multivariate_normal` must be a float "
                     f"dtype, got {dtype}")
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "multivariate_normal", shape)
  return maybe_auto_axes(_multivariate_normal, out_sharding,
                         shape=shape, dtype=dtype)(key, mean, cov, method=method)

