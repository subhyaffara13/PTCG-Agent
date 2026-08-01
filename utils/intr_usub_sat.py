
def intr_usub_sat(a: _ods_ir.Value, b: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return USubSat(a=a, b=b, results=results, loc=loc, ip=ip).result

