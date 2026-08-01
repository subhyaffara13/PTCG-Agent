
def Gamma(name, k, theta):
    r"""
    Create a continuous random variable with a Gamma distribution.

    Explanation
    ===========

    The density of the Gamma distribution is given by

    .. math::
        f(x) := \frac{1}{\Gamma(k) \theta^k} x^{k - 1} e^{-\frac{x}{\theta}}

    with :math:`x \in [0,1]`.

    Parameters
    ==========

    k : Real number, `k > 0`, a shape
    theta : Real number, `\theta > 0`, a scale

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Gamma, density, cdf, E, variance
    >>> from sympy import Symbol, pprint, simplify

    >>> k = Symbol("k", positive=True)
    >>> theta = Symbol("theta", positive=True)
    >>> z = Symbol("z")

    >>> X = Gamma("x", k, theta)

    >>> D = density(X)(z)
    >>> pprint(D, use_unicode=False)
                      -z
                    -----
         -k  k - 1  theta
    theta  *z     *e
    ---------------------
           Gamma(k)

    >>> C = cdf(X, meijerg=True)(z)
    >>> pprint(C, use_unicode=False)
    /            /     z  \
    |k*lowergamma|k, -----|
    |            \   theta/
    <----------------------  for z >= 0
    |     Gamma(k + 1)
    |
    \          0             otherwise

    >>> E(X)
    k*theta

    >>> V = simplify(variance(X))
    >>> pprint(V, use_unicode=False)
           2
    k*theta


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Gamma_distribution
    .. [2] https://mathworld.wolfram.com/GammaDistribution.html

    """

    return rv(name, GammaDistribution, (k, theta))


def gamma(key: ArrayLike,
          a: RealArray,
          shape: Shape | None = None,
          dtype: DTypeLikeFloat | None = None,
          *,
          out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Gamma random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x;a) \propto x^{a - 1} e^{-x}

  on the domain :math:`0 \le x < \infty`, with :math:`a > 0`.

  This is the standard gamma density, with a unit scale/rate parameter.
  Dividing the sample output by the rate is equivalent to sampling from
  *gamma(a, rate)*, and multiplying the sample output by the scale is equivalent
  to sampling from *gamma(a, scale)*.

  Args:
    key: a PRNG key used as the random key.
    a: a float or array of floats broadcast-compatible with ``shape``
      representing the parameter of the distribution.
    shape: optional, a tuple of nonnegative integers specifying the result
      shape. Must be broadcast-compatible with ``a``. The default (None)
      produces a result shape equal to ``a.shape``.
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
    A random array with the specified dtype and with shape given by ``shape`` if
    ``shape`` is not None, or else by ``a.shape``.

  See Also:
    loggamma : sample gamma values in log-space, which can provide improved
      accuracy for small values of ``a``.
  """
  key, _ = _check_prng_key("gamma", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `gamma` must be a float "
                     f"dtype, got {dtype}")
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "gamma", shape)
  return maybe_auto_axes(_gamma, out_sharding, shape=shape, dtype=dtype)(key, a)


def gamma(x: ArrayLike) -> Array:
  r"""The gamma function.

  JAX implementation of :obj:`scipy.special.gamma`.

  The gamma function is defined for :math:`\Re(z)>0` as

  .. math::

     \mathrm{gamma}(z) = \Gamma(z) = \int_0^\infty t^{z-1}e^{-t}\mathrm{d}t

  and is extended by analytic continuation to arbitrary complex values `z`.
  For positive integers `n`, the gamma function is related to the
  :func:`~jax.scipy.special.factorial` function via the following identity:

  .. math::

     \Gamma(n) = (n - 1)!

  For real inputs:

  * if :math:`x = -\infty`, NaN is returned.
  * if :math:`x = \pm 0`, :math:`\pm \infty` is returned.
  * if :math:`x` is a negative integer, NaN is returned. The sign of gamma
    at a negative integer depends on from which side the pole is approached.
  * if :math:`x = \infty`, :math:`\infty` is returned.
  * if :math:`x` is NaN, NaN is returned.

  For complex inputs:

  * at non-positive integers (poles), ``nan+nanj`` is returned, matching SciPy.
  * if either real or imaginary component is NaN, ``nan+nanj`` is returned.

  Args:
    x: arraylike, real or complex valued. Complex inputs use a Lanczos
       approximation with reflection formula.

  Returns:
    array containing the values of the gamma function. For complex inputs,
    the output is complex-valued.

  See Also:
    - :func:`jax.scipy.special.factorial`: the factorial function.
    - :func:`jax.scipy.special.gammaln`: the natural log of the gamma function
    - :func:`jax.scipy.special.gammasgn`: the sign of the gamma function

  Notes:
    For complex inputs, the implementation uses the Lanczos approximation
    (g=7, N=9 coefficients) with the reflection formula for Re(z) < 0.5.
  """
  x, = promote_args_inexact("gamma", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return _complex_gamma(x)
  return gammasgn(x) * lax.exp(lax.lgamma(x))

