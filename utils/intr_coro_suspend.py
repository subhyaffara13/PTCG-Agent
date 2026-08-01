
def intr_coro_suspend(res: _ods_ir.Type, save: _ods_ir.Value, final: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CoroSuspendOp(res=res, save=save, final=final, loc=loc, ip=ip).result

