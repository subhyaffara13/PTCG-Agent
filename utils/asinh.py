
def asinh(a):
    return prims.asinh(a)


def asinh(x):
    """Evaluates the inverse hyperbolic sine of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        return interval(np.arcsinh(x))
    elif isinstance(x, interval):
        start = np.arcsinh(x.start)
        end = np.arcsinh(x.end)
        return interval(start, end, is_valid=x.is_valid)
    else:
        return NotImplementedError


def asinh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsinhOp(operand=operand, results=results, loc=loc, ip=ip).result


def asinh(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsinhOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def asinh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsinhOp(operand=operand, results=results, loc=loc, ip=ip).result


def asinh(x: ArrayLike) -> Array:
  r"""Elementwise inverse hyperbolic sine: :math:`\mathrm{asinh}(x)`.

  This function lowers directly to the ``chlo.asinh`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    inverse hyperbolic sine.

  See also:
    - :func:`jax.lax.acosh`: elementwise inverse hyperbolic cosine.
    - :func:`jax.lax.atanh`: elementwise inverse hyperbolic tangent.
    - :func:`jax.lax.sinh`: elementwise hyperbolic sine.
  """
  return asinh_p.bind(x)


def asinh(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arcsinh`"""
  return arcsinh(*promote_args('asinh', x))

