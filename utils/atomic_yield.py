
def atomic_yield(result: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> AtomicYieldOp:
  return AtomicYieldOp(result=result, loc=loc, ip=ip)

