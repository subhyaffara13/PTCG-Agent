
def mbarrier_arrive_drop(addr: _ods_ir.Value, *, count: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, scope: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relaxed: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, MBarrierArriveDropOp]:
  op = MBarrierArriveDropOp(addr=addr, count=count, scope=scope, relaxed=relaxed, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

