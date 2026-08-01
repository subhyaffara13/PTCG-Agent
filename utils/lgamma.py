
def lgamma(a):
    return prims.lgamma(a)


def lgamma(operand: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LgammaOp(operand=operand, results=results, loc=loc, ip=ip).result


def lgamma(x): return scipy.special.gammaln(x).astype(x.dtype)


def lgamma(x: ArrayLike) -> Array:
  r"""Elementwise log gamma: :math:`\mathrm{log}(\Gamma(x))`."""
  return lgamma_p.bind(x)

