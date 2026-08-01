
def mbarrier_create(barriers: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MBarrierCreateOp(barriers=barriers, loc=loc, ip=ip).result

