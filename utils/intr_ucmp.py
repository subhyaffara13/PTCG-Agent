
def intr_ucmp(res: _ods_ir.Type, a: _ods_ir.Value, b: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return UCmpOp(res=res, a=a, b=b, loc=loc, ip=ip).result

