
def intr_coro_resume(handle: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CoroResumeOp:
  return CoroResumeOp(handle=handle, loc=loc, ip=ip)

