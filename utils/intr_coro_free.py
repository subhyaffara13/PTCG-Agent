
def intr_coro_free(res: _ods_ir.Type, id: _ods_ir.Value, handle: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoroFreeOp(res=res, id=id, handle=handle, loc=loc, ip=ip).result

