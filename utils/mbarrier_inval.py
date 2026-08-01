
def mbarrier_inval(addr: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MBarrierInvalOp:
  return MBarrierInvalOp(addr=addr, loc=loc, ip=ip)

