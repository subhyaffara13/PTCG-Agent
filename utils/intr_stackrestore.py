
def intr_stackrestore(ptr: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StackRestoreOp:
  return StackRestoreOp(ptr=ptr, loc=loc, ip=ip)

