
def transfer(result: _ods_ir.Type, tensor: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TransferOp(result=result, tensor=tensor, loc=loc, ip=ip).result

