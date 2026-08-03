import logging
import sys

def log(a):
    return prims.log(a)


def log(g: jit_utils.GraphContext, self):
    return g.op("Log", self)


def log(x):
    """evaluates the natural logarithm of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        if x <= 0:
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            return interval(np.log(x))
    elif isinstance(x, interval):
        if not x.is_valid:
            return interval(-np.inf, np.inf, is_valid=x.is_valid)
        elif x.end <= 0:
            return interval(-np.inf, np.inf, is_valid=False)
        elif x.start <= 0:
            return interval(-np.inf, np.inf, is_valid=None)

        return interval(np.log(x.start), np.log(x.end))
    else:
        raise NotImplementedError


def log(X, /):
    r"""Natural logarithm of a non-negative random variable.

    Parameters
    ----------
    X : `ContinuousDistribution`
        The random variable :math:`X` with positive support.

    Returns
    -------
    Y : `ContinuousDistribution`
        A random variable :math:`Y = \log(X)`.

    Examples
    --------
    Suppose we have a gamma distributed random variable :math:`X`:

    >>> import numpy as np
    >>> from scipy import stats
    >>> Gamma = stats.make_distribution(stats.gamma)
    >>> X = Gamma(a=1.0)

    We wish to have an exp-gamma distributed random variable :math:`Y`,
    a random variable whose natural exponential is :math:`X`.
    If :math:`X` is to be the natural exponential of :math:`Y`, then we
    must take :math:`Y` to be the natural logarithm of :math:`X`.

    >>> Y = stats.log(X)

    To demonstrate that ``X`` represents the exponential of ``Y``,
    we plot a normalized histogram of the exponential of observations of
    ``Y`` against the PDF underlying ``X``.

    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng(435383595582522)
    >>> y = Y.sample(shape=10000, rng=rng)
    >>> ax = plt.gca()
    >>> ax.hist(np.exp(y), bins=50, density=True)
    >>> X.plot(ax=ax)
    >>> plt.legend(('PDF of `X`', 'histogram of `exp(y)`'))
    >>> plt.show()

    """
    if np.any(X.support()[0] < 0):
        message = ("The logarithm of a random variable is only implemented when the "
                   "support is non-negative.")
        raise NotImplementedError(message)
    return MonotonicTransformedDistribution(X, g=np.log, h=np.exp, dh=np.exp,
                                            logdh=lambda u: u)


def log(msg, *args, **kwargs):
    '''Log a message, passing *args* to the strings' `format()` method.

    *indent*, if present as a keyword argument, specifies the indent level, so
    that `indent=0` will log normally, `indent=1` will indent the message by 4
    spaces, &c..
    *noformat*, if present and True, will cause the message not to be formatted
    in any way.
    '''
    indent = 4 * kwargs.get('indent', 0)
    delimiter = kwargs.get('delimiter', '\n')
    m = msg if kwargs.get('noformat', False) else msg.format(*args)
    stream = kwargs.get('stream', sys.stdout)
    stream.write(' ' * indent + m + delimiter)


def log(x):
    """
    Compute the natural logarithm of `x`.

    Return the "principal value" (for a description of this, see `numpy.log`)
    of :math:`log_e(x)`. For real `x > 0`, this is a real number (``log(0)``
    returns ``-inf`` and ``log(np.inf)`` returns ``inf``). Otherwise, the
    complex principle value is returned.

    Parameters
    ----------
    x : array_like
       The value(s) whose log is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The log of the `x` value(s). If `x` was a scalar, so is `out`,
       otherwise an array is returned.

    See Also
    --------
    numpy.log

    Notes
    -----
    For a log() that returns ``NAN`` when real `x < 0`, use `numpy.log`
    (note, however, that otherwise `numpy.log` and this `log` are identical,
    i.e., both return ``-inf`` for `x = 0`, ``inf`` for `x = inf`, and,
    notably, the complex principle value if ``x.imag != 0``).

    Examples
    --------
    >>> import numpy as np
    >>> np.emath.log(np.exp(1))
    1.0

    Negative arguments are handled "correctly" (recall that
    ``exp(log(x)) == x`` does *not* hold for real ``x < 0``):

    >>> np.emath.log(-np.exp(1)) == (1 + np.pi * 1j)
    True

    """
    x = _fix_real_lt_zero(x)
    return nx.log(x)


def log(ctx, x, b=None):
    if b is None:
        return ctx.ln(x)
    wp = ctx.prec + 20
    return ctx.ln(x, prec=wp) / ctx.ln(b, prec=wp)


def log(inputs: _Sequence[_ods_ir.Value], tag: _Union[str, _ods_ir.StringAttr], *, formatted: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> LogOp:
  return LogOp(inputs=inputs, tag=tag, formatted=formatted, loc=loc, ip=ip)


def log(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LogOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def log(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return LogOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def log(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return LogOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def log(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise natural logarithm: :math:`\mathrm{log}(x)`.

  This function lowers directly to the  `stablehlo.log`_ operation.

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
    natural logarithm.

  See also:
    - :func:`jax.lax.exp`: elementwise exponentional: :math:`e^x`.

  .. _stablehlo.log: https://openxla.org/stablehlo/spec#log
  """
  return log_p.bind(x, accuracy=accuracy)


def log(x: ArrayLike, /) -> Array:
  """Calculate element-wise natural logarithm of the input.

  JAX implementation of :obj:`numpy.log`.

  Args:
    x: input array or scalar.

  Returns:
    An array containing the logarithm of each element in ``x``, promotes to inexact
    dtype.

  See also:
    - :func:`jax.numpy.exp`: Calculates element-wise exponential of the input.
    - :func:`jax.numpy.log2`: Calculates base-2 logarithm of each element of input.
    - :func:`jax.numpy.log1p`: Calculates element-wise logarithm of one plus input.

  Examples:
    ``jnp.log`` and ``jnp.exp`` are inverse functions of each other. Applying
    ``jnp.log`` on the result of ``jnp.exp(x)`` yields the original input ``x``.

    >>> x = jnp.array([2, 3, 4, 5])
    >>> jnp.log(jnp.exp(x))
    Array([2., 3., 4., 5.], dtype=float32)

    Using ``jnp.log`` we can demonstrate well-known properties of logarithms, such
    as :math:`log(a*b) = log(a)+log(b)`.

    >>> x1 = jnp.array([2, 1, 3, 1])
    >>> x2 = jnp.array([1, 3, 2, 4])
    >>> jnp.allclose(jnp.log(x1*x2), jnp.log(x1)+jnp.log(x2))
    Array(True, dtype=bool)
  """
  out = lax.log(*promote_args_inexact('log', x))
  jnp_error._set_error_if_nan(out)
  return out


def log(level, msg, *args, **kwargs):
  """Logs ``msg % args`` at absl logging level ``level``.

  If no args are given just print msg, ignoring any interpolation specifiers.

  Args:
    level: int, the absl logging level at which to log the message
        (logging.DEBUG|INFO|WARNING|ERROR|FATAL). While some C++ verbose logging
        level constants are also supported, callers should prefer explicit
        logging.vlog() calls for such purpose.

    msg: str, the message to be logged.
    *args: The args to be substituted into the msg.
    **kwargs: May contain exc_info to add exception traceback to message.
  """
  if level > converter.ABSL_DEBUG:
    # Even though this function supports level that is greater than 1, users
    # should use logging.vlog instead for such cases.
    # Treat this as vlog, 1 is equivalent to DEBUG.
    standard_level = converter.STANDARD_DEBUG - (level - 1)
  else:
    if level < converter.ABSL_FATAL:
      level = converter.ABSL_FATAL
    standard_level = converter.absl_to_standard(level)

  # Match standard logging's behavior. Before use_absl_handler() and
  # logging is configured, there is no handler attached on _absl_logger nor
  # logging.root. So logs go no where.
  if not logging.root.handlers:
    logging.basicConfig()

  _absl_logger.log(standard_level, msg, *args, **kwargs)

