
def atan(a):
    return prims.atan(a)


def atan(g: jit_utils.GraphContext, self):
    return g.op("Atan", self)


def atan(x):
    """evaluates the tan inverse of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.arctan(x))
    elif isinstance(x, interval):
        start = np.arctan(x.start)
        end = np.arctan(x.end)
        return interval(start, end, is_valid=x.is_valid)
    else:
        raise NotImplementedError


def atan(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtanOp(operand=operand, results=results, loc=loc, ip=ip).result


def atan(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtanOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def atan(x: ArrayLike) -> Array:
  r"""Elementwise arc tangent: :math:`\mathrm{atan}(x)`.

  This function lowers directly to the ``chlo.atan`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the
    element-wise arc tangent.

  See also:
    - :func:`jax.lax.tan`: elementwise tangent.
    - :func:`jax.lax.acos`: elementwise arc cosine.
    - :func:`jax.lax.asin`: elementwise arc sine.
    - :func:`jax.lax.atan2`: elementwise 2-term arc tangent.
  """
  return atan_p.bind(x)


def atan(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arctan`"""
  return arctan(*promote_args('atan', x))

