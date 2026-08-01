
def acosh(a):
    return prims.acosh(a)


def acosh(x):
    """Evaluates the inverse hyperbolic cosine of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        #Outside the domain
        if x < 1:
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            return interval(np.arccosh(x))
    elif isinstance(x, interval):
        #Outside the domain
        if x.end < 1:
            return interval(-np.inf, np.inf, is_valid=False)
        #Partly outside the domain
        elif x.start < 1:
            return interval(-np.inf, np.inf, is_valid=None)
        else:
            start = np.arccosh(x.start)
            end = np.arccosh(x.end)
            return interval(start, end, is_valid=x.is_valid)
    else:
        return NotImplementedError


def acosh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AcoshOp(operand=operand, results=results, loc=loc, ip=ip).result


def acosh(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AcoshOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def acosh(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AcoshOp(operand=operand, results=results, loc=loc, ip=ip).result


def acosh(x: ArrayLike) -> Array:
  r"""Elementwise inverse hyperbolic cosine: :math:`\mathrm{acosh}(x)`.

  This function lowers directly to the ``chlo.acosh`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the element-wise
    inverse hyperbolic cosine.

  See also:
    - :func:`jax.lax.asinh`: elementwise inverse hyperbolic sine.
    - :func:`jax.lax.atanh`: elementwise inverse hyperbolic tangent.
    - :func:`jax.lax.cosh`: elementwise hyperbolic cosine.
  """
  return acosh_p.bind(x)


def acosh(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arccosh`"""
  return arccosh(*promote_args('acosh', x))

