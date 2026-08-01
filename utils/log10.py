
def log10(a):
    return prims.log10(a)


def log10(g: jit_utils.GraphContext, self):
    _ln10 = 2.30258509299404568401
    return g.op("Div", log(g, self), g.op("Constant", value_t=torch.tensor([_ln10])))


def log10(x):
    """evaluates the logarithm to the base 10 of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        if x <= 0:
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            return interval(np.log10(x))
    elif isinstance(x, interval):
        if not x.is_valid:
            return interval(-np.inf, np.inf, is_valid=x.is_valid)
        elif x.end <= 0:
            return interval(-np.inf, np.inf, is_valid=False)
        elif x.start <= 0:
            return interval(-np.inf, np.inf, is_valid=None)
        return interval(np.log10(x.start), np.log10(x.end))
    else:
        raise NotImplementedError


def log10(x):
    """
    Compute the logarithm base 10 of `x`.

    Return the "principal value" (for a description of this, see
    `numpy.log10`) of :math:`log_{10}(x)`. For real `x > 0`, this
    is a real number (``log10(0)`` returns ``-inf`` and ``log10(np.inf)``
    returns ``inf``). Otherwise, the complex principle value is returned.

    Parameters
    ----------
    x : array_like or scalar
       The value(s) whose log base 10 is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The log base 10 of the `x` value(s). If `x` was a scalar, so is `out`,
       otherwise an array object is returned.

    See Also
    --------
    numpy.log10

    Notes
    -----
    For a log10() that returns ``NAN`` when real `x < 0`, use `numpy.log10`
    (note, however, that otherwise `numpy.log10` and this `log10` are
    identical, i.e., both return ``-inf`` for `x = 0`, ``inf`` for `x = inf`,
    and, notably, the complex principle value if ``x.imag != 0``).

    Examples
    --------
    >>> import numpy as np

    (We set the printing precision so the example can be auto-tested)

    >>> np.set_printoptions(precision=4)

    >>> np.emath.log10(10**1)
    1.0

    >>> np.emath.log10([-10**1, -10**2, 10**2])
    array([1.+1.3644j, 2.+1.3644j, 2.+0.j    ])

    """
    x = _fix_real_lt_zero(x)
    return nx.log10(x)


def log10(ctx, x):
    return ctx.log(x, 10)


def log10(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return Log10Op(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def log10(x: ArrayLike, /) -> Array:
  """Calculates the base-10 logarithm of x element-wise

  JAX implementation of :obj:`numpy.log10`.

  Args:
    x: Input array

  Returns:
    An array containing the base-10 logarithm of each element in ``x``, promotes
    to inexact dtype.

  Examples:
    >>> x1 = jnp.array([0.01, 0.1, 1, 10, 100, 1000])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.log10(x1))
    [-2. -1.  0.  1.  2.  3.]
  """
  x, = promote_args_inexact("log10", x)
  one_over_log10 = np.array(0.4342944819032518,  # exact value of 1 / log(10)
                            dtype=dtypes.finfo(x.dtype).dtype)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    r = lax.log(x)
    re = lax.real(r)
    im = lax.imag(r)
    return lax.complex(lax.mul(re, one_over_log10), lax.mul(im, one_over_log10))
  out = lax.mul(lax.log(x), one_over_log10)
  jnp_error._set_error_if_nan(out)
  return out

