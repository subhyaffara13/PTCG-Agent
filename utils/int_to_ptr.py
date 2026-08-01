
def int_to_ptr(result: _ods_ir.Type, src: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IntToPtrOp(result=result, src=src, loc=loc, ip=ip).result

