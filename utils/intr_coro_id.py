
def intr_coro_id(res: _ods_ir.Type, align: _ods_ir.Value[_ods_ir.IntegerType], promise: _ods_ir.Value, coroaddr: _ods_ir.Value, fnaddrs: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoroIdOp(res=res, align=align, promise=promise, coroaddr=coroaddr, fnaddrs=fnaddrs, loc=loc, ip=ip).result

