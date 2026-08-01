
def intr_debugtrap(*, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DebugTrap:
  return DebugTrap(loc=loc, ip=ip)

