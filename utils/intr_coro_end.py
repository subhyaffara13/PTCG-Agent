
def intr_coro_end(res: _ods_ir.Type, handle: _ods_ir.Value, unwind: _ods_ir.Value[_ods_ir.IntegerType], retvals: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoroEndOp(res=res, handle=handle, unwind=unwind, retvals=retvals, loc=loc, ip=ip).result

