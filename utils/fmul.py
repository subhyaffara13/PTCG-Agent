
def fmul(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FMulOp(lhs=lhs, rhs=rhs, fastmathFlags=fastmath_flags, results=results, loc=loc, ip=ip).result

