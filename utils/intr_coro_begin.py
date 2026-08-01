
def intr_coro_begin(res: _ods_ir.Type, token: _ods_ir.Value, mem: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoroBeginOp(res=res, token=token, mem=mem, loc=loc, ip=ip).result

