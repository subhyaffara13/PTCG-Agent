
def Logistic(name, mu, s):
    r"""
    Create a continuous random variable with a logistic distribution.

    Explanation
    ===========

    The density of the logistic distribution is given by

    .. math::
        f(x) := \frac{e^{-(x-\mu)/s}} {s\left(1+e^{-(x-\mu)/s}\right)^2}

    Parameters
    ==========

    mu : Real number, the location (mean)
    s : Real number, `s > 0`, a scale

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Logistic, density, cdf
    >>> from sympy import Symbol

    >>> mu = Symbol("mu", real=True)
    >>> s = Symbol("s", positive=True)
    >>> z = Symbol("z")

    >>> X = Logistic("x", mu, s)

    >>> density(X)(z)
    exp((mu - z)/s)/(s*(exp((mu - z)/s) + 1)**2)

    >>> cdf(X)(z)
    1/(exp((mu - z)/s) + 1)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Logistic_distribution
    .. [2] https://mathworld.wolfram.com/LogisticDistribution.html

    """

    return rv(name, LogisticDistribution, (mu, s))


def logistic(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return LogisticOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def logistic(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return LogisticOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def logistic(x): return (1 / (1 + np.exp(-x))).astype(x.dtype)


def logistic(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise logistic (sigmoid) function: :math:`\frac{1}{1 + e^{-x}}`.

  There is no HLO logistic/sigmoid primitive, so this lowers to a sequence
  of HLO arithmetic operations.

  Args:
    x: input array. Must have floating point or complex dtype.
    accuracy: Optional `lax.Tolerance` or `lax.AccuracyMode` object that
      selects the implementation of the op based on the requested accuracy. If
      the implementation cannot satisfy the requested tolerance, the
      compiler will return an error. If mode is specified and there are no
      multiple implementations available, the default implementation will be
      used.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    logistic/sigmoid function.

  See also:
    - :func:`jax.nn.sigmoid`: an alternative API for this functionality.
  """
  return logistic_p.bind(x, accuracy=accuracy)


def logistic(key: ArrayLike,
             shape: Shape = (),
             dtype: DTypeLikeFloat | None = None,
             *,
             out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample logistic random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x) = \frac{e^{-x}}{(1 + e^{-x})^2}

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
  key, _ = _check_prng_key("logistic", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `logistic` must be a float "
                     f"dtype, got {dtype}")
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "logistic", shape)
  return maybe_auto_axes(_logistic, out_sharding,
                         shape=shape, dtype=dtype)(key)

