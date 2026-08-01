
def mbarrier_init(barriers: _ods_ir.Value, count: _ods_ir.Value[_ods_ir.IndexType], mbar_id: _ods_ir.Value[_ods_ir.IndexType], *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MBarrierInitOp:
  return MBarrierInitOp(barriers=barriers, count=count, mbarId=mbar_id, predicate=predicate, loc=loc, ip=ip)


def mbarrier_init(addr: _ods_ir.Value, count: _ods_ir.Value[_ods_ir.IntegerType], *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MBarrierInitOp:
  return MBarrierInitOp(addr=addr, count=count, predicate=predicate, loc=loc, ip=ip)

