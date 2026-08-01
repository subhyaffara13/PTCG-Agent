
def shl(lhs: _ods_ir.Value, rhs: _ods_ir.Value, overflow_flags, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ShlOp(lhs=lhs, rhs=rhs, overflowFlags=overflow_flags, results=results, loc=loc, ip=ip).result

