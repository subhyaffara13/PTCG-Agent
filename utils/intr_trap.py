
def intr_trap(*, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Trap:
  return Trap(loc=loc, ip=ip)

