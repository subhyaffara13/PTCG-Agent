
def mlir_zero(res: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ZeroOp(res=res, loc=loc, ip=ip).result

