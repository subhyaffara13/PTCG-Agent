
def intr_fma(a: _ods_ir.Value, b: _ods_ir.Value, c: _ods_ir.Value, *, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FMAOp(a=a, b=b, c=c, fastmathFlags=fastmath_flags, results=results, loc=loc, ip=ip).result

