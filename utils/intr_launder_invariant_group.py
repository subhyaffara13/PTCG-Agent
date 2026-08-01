
def intr_launder_invariant_group(ptr: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LaunderInvariantGroupOp(ptr=ptr, results=results, loc=loc, ip=ip).result

