
def mbarrier_arrive_expect_tx(barriers: _ods_ir.Value, txcount: _ods_ir.Value[_ods_ir.IndexType], mbar_id: _ods_ir.Value[_ods_ir.IndexType], *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MBarrierArriveExpectTxOp:
  return MBarrierArriveExpectTxOp(barriers=barriers, txcount=txcount, mbarId=mbar_id, predicate=predicate, loc=loc, ip=ip)


def mbarrier_arrive_expect_tx(addr: _ods_ir.Value, txcount: _ods_ir.Value[_ods_ir.IntegerType], *, scope: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relaxed: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, MBarrierArriveExpectTxOp]:
  op = MBarrierArriveExpectTxOp(addr=addr, txcount=txcount, scope=scope, relaxed=relaxed, predicate=predicate, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

