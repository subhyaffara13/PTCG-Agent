
def intr_lifetime_end(ptr: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> LifetimeEndOp:
  return LifetimeEndOp(ptr=ptr, loc=loc, ip=ip)

