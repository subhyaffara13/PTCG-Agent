
def Laplace(name, mu, b):
    r"""
    Create a continuous random variable with a Laplace distribution.

    Explanation
    ===========

    The density of the Laplace distribution is given by

    .. math::
        f(x) := \frac{1}{2 b} \exp \left(-\frac{|x-\mu|}b \right)

    Parameters
    ==========

    mu : Real number or a list/matrix, the location (mean) or the
        location vector
    b : Real number or a positive definite matrix, representing a scale
        or the covariance matrix.

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Laplace, density, cdf
    >>> from sympy import Symbol, pprint

    >>> mu = Symbol("mu")
    >>> b = Symbol("b", positive=True)
    >>> z = Symbol("z")

    >>> X = Laplace("x", mu, b)

    >>> density(X)(z)
    exp(-Abs(mu - z)/b)/(2*b)

    >>> cdf(X)(z)
    Piecewise((exp((-mu + z)/b)/2, mu > z), (1 - exp((mu - z)/b)/2, True))

    >>> L = Laplace('L', [1, 2], [[1, 0], [0, 1]])
    >>> pprint(density(L)(1, 2), use_unicode=False)
     5        /     ____\
    e *besselk\0, \/ 35 /
    ---------------------
              pi

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Laplace_distribution
    .. [2] https://mathworld.wolfram.com/LaplaceDistribution.html

    """

    if isinstance(mu, (list, MatrixBase)) and\
        isinstance(b, (list, MatrixBase)):
        from sympy.stats.joint_rv_types import MultivariateLaplace
        return MultivariateLaplace(name, mu, b)

    return rv(name, LaplaceDistribution, (mu, b))


def laplace(input, output=None, mode="reflect", cval=0.0, *, axes=None):
    """N-D Laplace filter based on approximate second derivatives.

    Parameters
    ----------
    %(input)s
    %(output)s
    %(mode_multiple)s
    %(cval)s
    axes : tuple of int or None
        The axes over which to apply the filter. If a `mode` tuple is
        provided, its length must match the number of axes.

    Returns
    -------
    laplace : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.laplace(ascent)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    def derivative2(input, axis, output, mode, cval):
        return correlate1d(input, [1, -2, 1], axis, output, mode, cval, 0)
    return generic_laplace(input, derivative2, output, mode, cval, axes=axes)


def laplace(key: ArrayLike,
            shape: Shape = (),
            dtype: DTypeLikeFloat | None = None,
            *,
            out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Laplace random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
    f(x) = \frac{1}{2}e^{-|x|}

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key("laplace", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `laplace` must be a float "
                     f"dtype, got {dtype}")
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "laplace", shape)
  return maybe_auto_axes(_laplace, out_sharding,
                         shape=shape, dtype=dtype)(key)

