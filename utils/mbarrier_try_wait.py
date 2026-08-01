
def mbarrier_try_wait(addr: _ods_ir.Value, state_or_phase: _ods_ir.Value, *, ticks: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, scope: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relaxed: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return MBarrierTryWaitOp(addr=addr, stateOrPhase=state_or_phase, ticks=ticks, scope=scope, relaxed=relaxed, results=results, loc=loc, ip=ip).result

