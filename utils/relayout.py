
def relayout(input: _ods_ir.Value[_ods_ir.VectorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return RelayoutOp(input=input, results=results, loc=loc, ip=ip).result

