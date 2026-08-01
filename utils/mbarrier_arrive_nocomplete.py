
def mbarrier_arrive_nocomplete(barriers: _ods_ir.Value, mbar_id: _ods_ir.Value[_ods_ir.IndexType], count: _ods_ir.Value[_ods_ir.IndexType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MBarrierArriveNoCompleteOp(barriers=barriers, mbarId=mbar_id, count=count, results=results, loc=loc, ip=ip).result


def mbarrier_arrive_nocomplete(addr: _ods_ir.Value, count: _ods_ir.Value[_ods_ir.IntegerType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return MBarrierArriveNocompleteOp(addr=addr, count=count, results=results, loc=loc, ip=ip).result

