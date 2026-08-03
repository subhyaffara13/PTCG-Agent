import math


def exp(a):
    return prims.exp(a)


def exp(x, use_fast_math: tl.constexpr):
    if use_fast_math:
        return math.exp(x)
    else:
        return libdevice.exp(x)


def exp(g: jit_utils.GraphContext, self):
    return g.op("Exp", self)


def exp(x):
    """evaluates the exponential of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.exp(x), np.exp(x))
    elif isinstance(x, interval):
        return interval(np.exp(x.start), np.exp(x.end), is_valid=x.is_valid)
    else:
        raise NotImplementedError


def exp(X, /):
    r"""Natural exponential of a random variable.

    Parameters
    ----------
    X : `ContinuousDistribution`
        The random variable :math:`X`.

    Returns
    -------
    Y : `ContinuousDistribution`
        A random variable :math:`Y = \exp(X)`.

    Examples
    --------
    Suppose we have a normally distributed random variable :math:`X`:

    >>> import numpy as np
    >>> from scipy import stats
    >>> X = stats.Normal()

    We wish to have a lognormally distributed random variable :math:`Y`,
    a random variable whose natural logarithm is :math:`X`.
    If :math:`X` is to be the natural logarithm of :math:`Y`, then we
    must take :math:`Y` to be the natural exponential of :math:`X`.

    >>> Y = stats.exp(X)

    To demonstrate that ``X`` represents the logarithm of ``Y``,
    we plot a normalized histogram of the logarithm of observations of
    ``Y`` against the PDF underlying ``X``.

    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng(435383595582522)
    >>> y = Y.sample(shape=10000, rng=rng)
    >>> ax = plt.gca()
    >>> ax.hist(np.log(y), bins=50, density=True)
    >>> X.plot(ax=ax)
    >>> plt.legend(('PDF of `X`', 'histogram of `log(y)`'))
    >>> plt.show()

    """
    return MonotonicTransformedDistribution(X, g=np.exp, h=np.log, dh=lambda u: 1 / u,
                                            logdh=lambda u: -np.log(u))


def exp(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExpOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def exp(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise exponential: :math:`e^x`.

  This function lowers directly to the  `stablehlo.exponential`_ operation.

  Args:
    x: input array. Must have floating-point or complex type.
    accuracy: Optional `lax.Tolerance` or `lax.AccuracyMode` object that
      selects the implementation of the op based on the requested accuracy. If
      the implementation cannot satisfy the requested tolerance, the
      compiler will return an error. If mode is specified and there are no
      multiple implementations available, the default implementation will be
      used.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    exponential.

  See also:
    - :func:`jax.lax.exp2`: elementwise base-2 exponentional: :math:`2^x`.
    - :func:`jax.lax.log`: elementwise natural logarithm: :math:`\mathrm{log}(x)`.

  .. _stablehlo.exponential: https://openxla.org/stablehlo/spec#exponential
  """
  return exp_p.bind(x, accuracy=accuracy)


def exp(x: ArrayLike, /) -> Array:
  """Calculate element-wise exponential of the input.

  JAX implementation of :obj:`numpy.exp`.

  Args:
    x: input array or scalar

  Returns:
    An array containing the exponential of each element in ``x``, promotes to
    inexact dtype.

  See also:
    - :func:`jax.numpy.log`: Calculates element-wise logarithm of the input.
    - :func:`jax.numpy.expm1`: Calculates :math:`e^x-1` of each element of the
      input.
    - :func:`jax.numpy.exp2`: Calculates base-2 exponential of each element of
      the input.

  Examples:
    ``jnp.exp`` follows the properties of exponential such as :math:`e^{(a+b)}
    = e^a * e^b`.

    >>> x1 = jnp.array([2, 4, 3, 1])
    >>> x2 = jnp.array([1, 3, 2, 3])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.exp(x1+x2))
    [  20.09 1096.63  148.41   54.6 ]
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.exp(x1)*jnp.exp(x2))
    [  20.09 1096.63  148.41   54.6 ]

    This property holds for complex input also:

    >>> jnp.allclose(jnp.exp(3-4j), jnp.exp(3)*jnp.exp(-4j))
    Array(True, dtype=bool)
  """
  return lax.exp(*promote_args_inexact('exp', x))

