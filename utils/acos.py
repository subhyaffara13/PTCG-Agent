
def acos(a):
    return prims.acos(a)


def acos(g: jit_utils.GraphContext, self):
    return g.op("Acos", self)


def acos(x):
    """Evaluates the inverse cos of an interval"""
    np = import_module('numpy')
    if isinstance(x, (int, float)):
        if abs(x) > 1:
            #Outside the domain
            return interval(-np.inf, np.inf, is_valid=False)
        else:
            return interval(np.arccos(x), np.arccos(x))
    elif isinstance(x, interval):
        #Outside the domain
        if x.is_valid is False or x.start > 1 or x.end < -1:
            return interval(-np.inf, np.inf, is_valid=False)
        #Partially outside the domain
        elif x.start < -1 or x.end > 1:
            return interval(-np.inf, np.inf, is_valid=None)
        else:
            start = np.arccos(x.start)
            end = np.arccos(x.end)
            return interval(start, end, is_valid=x.is_valid)


def acos(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AcosOp(operand=operand, results=results, loc=loc, ip=ip).result


def acos(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AcosOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def acos(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AcosOp(operand=operand, results=results, loc=loc, ip=ip).result


def acos(x: ArrayLike) -> Array:
  r"""Elementwise arc cosine: :math:`\mathrm{acos}(x)`.

  This function lowers directly to the ``chlo.acos`` operation.

  Args:
    x: input array. Must have floating-point or complex type.

  Returns:
    Array of the same shape and dtype as ``x`` containing the
    element-wise arc cosine.

  See also:
    - :func:`jax.lax.cos`: elementwise cosine.
    - :func:`jax.lax.asin`: elementwise arc sine.
    - :func:`jax.lax.atan`: elementwise arc tangent.
  """
  return acos_p.bind(x)


def acos(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.arccos`"""
  return arccos(*promote_args('acos', x))

