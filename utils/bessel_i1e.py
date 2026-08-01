
def bessel_i1e(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BesselI1eOp(operand=operand, results=results, loc=loc, ip=ip).result


def bessel_i1e(x): return scipy.special.i1e(x).astype(x.dtype)


def bessel_i1e(x: ArrayLike) -> Array:
  r"""Exponentially scaled modified Bessel function of order 1:
  :math:`\mathrm{i1e}(x) = e^{-|x|} \mathrm{i1}(x)`
  """
  return bessel_i1e_p.bind(x)

