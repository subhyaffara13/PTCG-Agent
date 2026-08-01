
def assume_layout(result: _ods_ir.Type, input: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AssumeLayoutOp(result=result, input=input, loc=loc, ip=ip).result

