
def intr_lifetime_start(ptr: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> LifetimeStartOp:
  return LifetimeStartOp(ptr=ptr, loc=loc, ip=ip)

