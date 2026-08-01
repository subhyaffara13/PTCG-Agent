
def intr_coro_promise(res: _ods_ir.Type, handle: _ods_ir.Value, align: _ods_ir.Value[_ods_ir.IntegerType], from_: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoroPromiseOp(res=res, handle=handle, align=align, from_=from_, loc=loc, ip=ip).result

