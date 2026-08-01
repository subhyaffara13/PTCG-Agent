
def mbarrier_arrive_drop_nocomplete(addr: _ods_ir.Value, count: _ods_ir.Value[_ods_ir.IntegerType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return MBarrierArriveDropNocompleteOp(addr=addr, count=count, results=results, loc=loc, ip=ip).result

