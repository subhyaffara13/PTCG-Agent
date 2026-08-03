import re

def loggamma(x):
    if type(x) not in (float, complex):
        try:
            x = float(x)
        except (ValueError, TypeError):
            x = complex(x)
    try:
        xreal = x.real
        ximag = x.imag
    except AttributeError:   # py2.5
        xreal = x
        ximag = 0.0
    # Reflection formula
    # http://functions.wolfram.com/GammaBetaErf/LogGamma/16/01/01/0003/
    if xreal < 0.0:
        if abs(x) < 0.5:
            v = log(gamma(x))
            if ximag == 0:
                v = v.conjugate()
            return v
        z = 1-x
        try:
            re = z.real
            im = z.imag
        except AttributeError:   # py2.5
            re = z
            im = 0.0
        refloor = floor(re)
        if im == 0.0:
            imsign = 0
        elif im < 0.0:
            imsign = -1
        else:
            imsign = 1
        return (-pi*1j)*abs(refloor)*(1-abs(imsign)) + logpi - \
            log(sinpi(z-refloor)) - loggamma(z) + 1j*pi*refloor*imsign
    if x == 1.0 or x == 2.0:
        return x*0
    p = 0.
    while abs(x) < 11:
        p -= log(x)
        x += 1.0
    s = 0.918938533204672742 + (x-0.5)*log(x) - x
    r = 1./x
    r2 = r*r
    s += 0.083333333333333333333*r; r *= r2
    s += -0.0027777777777777777778*r; r *= r2
    s += 0.00079365079365079365079*r; r *= r2
    s += -0.0005952380952380952381*r; r *= r2
    s += 0.00084175084175084175084*r; r *= r2
    s += -0.0019175269175269175269*r; r *= r2
    s += 0.0064102564102564102564*r; r *= r2
    s += -0.02955065359477124183*r
    return s + p


def loggamma(key: ArrayLike,
             a: RealArray,
             shape: Shape | None = None,
             dtype: DTypeLikeFloat | None = None,
             *,
             out_sharding: NamedSharding | P | None =None) -> Array:
  """Sample log-gamma random values with given shape and float dtype.

  This function is implemented such that the following will hold for a
  dtype-appropriate tolerance::

    np.testing.assert_allclose(jnp.exp(loggamma(*args)), gamma(*args), rtol=rtol)

  The benefit of log-gamma is that for samples very close to zero (which occur frequently
  when `a << 1`) sampling in log space provides better precision.

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
    gamma : standard gamma sampler.
  """
  key, _ = _check_prng_key("loggamma", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `gamma` must be a float "
                     f"dtype, got {dtype}")
  if shape is not None:
    shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding(out_sharding, "loggamma")
  return maybe_auto_axes(_gamma, out_sharding, shape=shape, dtype=dtype, log_space=True)(key, a)


def loggamma(x: ArrayLike) -> Array:
  r"""Principal branch of the logarithm of the gamma function.

  JAX implementation of :obj:`scipy.special.loggamma`.

  Defined to be :math:`\log(\Gamma(x))` for :math:`x > 0` and
  extended to the complex plane by analytic continuation. The
  function has a single branch cut on the negative real axis.

  Args:
    x: arraylike, real or complex valued.

  Returns:
    array containing the values of the loggamma function. For complex inputs,
    the output is complex-valued.

  See Also:
    - :func:`jax.scipy.special.gamma`: the gamma function.
    - :func:`jax.scipy.special.gammaln`: the natural log of the absolute value of the gamma function.
  """
  x, = promote_args_inexact("loggamma", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    return _complex_loggamma_scipy(x)
  res = lax.lgamma(x)
  return jnp.where(x > 0, res, jnp.nan)

