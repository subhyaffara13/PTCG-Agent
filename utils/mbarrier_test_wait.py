
def mbarrier_test_wait(barriers: _ods_ir.Value, token: _ods_ir.Value, mbar_id: _ods_ir.Value[_ods_ir.IndexType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return MBarrierTestWaitOp(barriers=barriers, token=token, mbarId=mbar_id, results=results, loc=loc, ip=ip).result


def mbarrier_test_wait(addr: _ods_ir.Value, state_or_phase: _ods_ir.Value, *, scope: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relaxed: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return MBarrierTestWaitOp(addr=addr, stateOrPhase=state_or_phase, scope=scope, relaxed=relaxed, results=results, loc=loc, ip=ip).result

