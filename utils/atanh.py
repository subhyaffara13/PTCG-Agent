
def atanh(a):
    return prims.atanh(a)


def atanh(x):
    """Evaluates the inverse hyperbolic tangent of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        #Outside the domain
        if abs(x) >= 1:
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            return interval(np.arctanh(x))
    elif isinstance(x, interval):
        #outside the domain
        if x.is_valid is False or x.start >= 1 or x.end <= -1:
            return interval(-np.inf, np.inf, is_valid=False)
        #partly outside the domain
        elif x.start <= -1 or x.end >= 1:
            return interval(-np.inf, np.inf, is_valid=None)
        else:
            start = np.arctanh(x.start)
            end = np.arctanh(x.end)
            return interval(start, end, is_valid=x.is_valid)
    else:
        return NotImplementedError


def atanh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtanhOp(operand=operand, results=results, loc=loc, ip=ip).result


def atanh(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtanhOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def atanh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtanhOp(operand=operand, results=results, loc=loc, ip=ip).result


def atanh(x: ArrayLike) -> Array:
  r"""Elementwise inverse hyperbolic tangent: :math:`\mathrm{atanh}(x)`.

  This function lowers directly to the ``chlo.atanh`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    inverse hyperbolic tangent.

  See also:
    - :func:`jax.lax.acosh`: elementwise inverse hyperbolic cosine.
    - :func:`jax.lax.asinh`: elementwise inverse hyperbolic sine.
    - :func:`jax.lax.tanh`: elementwise hyperbolic tangent.
  """
  return atanh_p.bind(x)


def atanh(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arctanh`"""
  return arctanh(*promote_args('atanh', x))

