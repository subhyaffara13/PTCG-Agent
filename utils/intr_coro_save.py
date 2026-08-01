
def intr_coro_save(res: _ods_ir.Type, handle: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoroSaveOp(res=res, handle=handle, loc=loc, ip=ip).result

