
def erf_inv(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ErfInvOp(operand=operand, results=results, loc=loc, ip=ip).result


def erf_inv(x): return scipy.special.erfinv(x).astype(x.dtype)


def erf_inv(x: ArrayLike) -> Array:
  r"""Elementwise inverse error function: :math:`\mathrm{erf}^{-1}(x)`."""
  return erf_inv_p.bind(x)

