
def mbarrier_try_wait_parity(barriers: _ods_ir.Value, phase_parity: _ods_ir.Value[_ods_ir.IntegerType], ticks: _ods_ir.Value[_ods_ir.IndexType], mbar_id: _ods_ir.Value[_ods_ir.IndexType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MBarrierTryWaitParityOp:
  return MBarrierTryWaitParityOp(barriers=barriers, phaseParity=phase_parity, ticks=ticks, mbarId=mbar_id, loc=loc, ip=ip)


def mbarrier_try_wait_parity(addr: _ods_ir.Value, phase: _ods_ir.Value[_ods_ir.IntegerType], ticks: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MBarrierTryWaitParityOp:
  return MBarrierTryWaitParityOp(addr=addr, phase=phase, ticks=ticks, loc=loc, ip=ip)

