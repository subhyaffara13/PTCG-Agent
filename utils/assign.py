
def assign(result: _ods_ir.Type, tensor: _ods_ir.Value, *, origin: _Optional[_Union[str, _ods_ir.StringAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AssignOp(result=result, tensor=tensor, origin=origin, loc=loc, ip=ip).result

