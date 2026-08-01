
def asin(a):
    return prims.asin(a)


def asin(g: jit_utils.GraphContext, self):
    return g.op("Asin", self)


def asin(x):
    """Evaluates the inverse sine of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        #Outside the domain
        if abs(x) > 1:
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            return interval(np.arcsin(x), np.arcsin(x))
    elif isinstance(x, interval):
        #Outside the domain
        if x.is_valid is False or x.start > 1 or x.end < -1:
            return interval(-np.inf, np.inf, is_valid=False)
        #Partially outside the domain
        elif x.start < -1 or x.end > 1:
            return interval(-np.inf, np.inf, is_valid=None)
        else:
            start = np.arcsin(x.start)
            end = np.arcsin(x.end)
            return interval(start, end, is_valid=x.is_valid)


def asin(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsinOp(operand=operand, results=results, loc=loc, ip=ip).result


def asin(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsinOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def asin(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsinOp(operand=operand, results=results, loc=loc, ip=ip).result


def asin(x: ArrayLike) -> Array:
  r"""Elementwise arc sine: :math:`\mathrm{asin}(x)`.

  This function lowers directly to the ``chlo.asin`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the
    element-wise arc sine.

  See also:
    - :func:`jax.lax.sin`: elementwise sine.
    - :func:`jax.lax.acos`: elementwise arc cosine.
    - :func:`jax.lax.atan`: elementwise arc tangent.
  """
  return asin_p.bind(x)


def asin(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arcsin`"""
  return arcsin(*promote_args('asin', x))

