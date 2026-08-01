
def intr_lround(res: _ods_ir.Type, val: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LroundOp(res=res, val=val, loc=loc, ip=ip).result

