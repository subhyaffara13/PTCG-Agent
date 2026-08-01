
def add_dependency(operand: _ods_ir.Value, token: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AddDependencyOp(operand=operand, token=token, results=results, loc=loc, ip=ip).result

