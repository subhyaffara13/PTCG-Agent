
def log2(a):
    return prims.log2(a)


def log2(g: jit_utils.GraphContext, self):
    _ln2 = 0.693147180559945309
    return g.op("Div", log(g, self), g.op("Constant", value_t=torch.tensor(_ln2)))


def log2(x):
    """
    Compute the logarithm base 2 of `x`.

    Return the "principal value" (for a description of this, see
    `numpy.log2`) of :math:`log_2(x)`. For real `x > 0`, this is
    a real number (``log2(0)`` returns ``-inf`` and ``log2(np.inf)`` returns
    ``inf``). Otherwise, the complex principle value is returned.

    Parameters
    ----------
    x : array_like
       The value(s) whose log base 2 is (are) required.

    Returns
    -------
    out : ndarray or scalar
       The log base 2 of the `x` value(s). If `x` was a scalar, so is `out`,
       otherwise an array is returned.

    See Also
    --------
    numpy.log2

    Notes
    -----
    For a log2() that returns ``NAN`` when real `x < 0`, use `numpy.log2`
    (note, however, that otherwise `numpy.log2` and this `log2` are
    identical, i.e., both return ``-inf`` for `x = 0`, ``inf`` for `x = inf`,
    and, notably, the complex principle value if ``x.imag != 0``).

    Examples
    --------

    We set the printing precision so the example can be auto-tested:

    >>> np.set_printoptions(precision=4)

    >>> np.emath.log2(8)
    3.0
    >>> np.emath.log2([-4, -8, 8])
    array([2.+4.5324j, 3.+4.5324j, 3.+0.j    ])

    """
    x = _fix_real_lt_zero(x)
    return nx.log2(x)


def log2(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return Log2Op(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def log2(src: _ods_ir.Value[_ods_ir.FloatType], *, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.FloatType]:
  return Log2Op(src=src, ftz=ftz, results=results, loc=loc, ip=ip).result


def log2(x: ArrayLike, /) -> Array:
  """Calculates the base-2 logarithm of ``x`` element-wise.

  JAX implementation of :obj:`numpy.log2`.

  Args:
    x: Input array

  Returns:
    An array containing the base-2 logarithm of each element in ``x``, promotes
    to inexact dtype.

  Examples:
    >>> x1 = jnp.array([0.25, 0.5, 1, 2, 4, 8])
    >>> jnp.log2(x1)
    Array([-2., -1.,  0.,  1.,  2.,  3.], dtype=float32)
  """
  x, = promote_args_inexact("log2", x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    r = lax.log(x)
    re = lax.real(r)
    im = lax.imag(r)
    ln2 = lax.log(_constant_like(re, 2))
    return lax.complex(lax.div(re, ln2), lax.div(im, ln2))
  out = lax.div(lax.log(x), lax.log(_constant_like(x, 2)))
  jnp_error._set_error_if_nan(out)
  return out

