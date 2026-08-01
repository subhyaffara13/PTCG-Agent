
def mbarrier_get(mbarrier_pointer: _ods_ir.Type, barriers: _ods_ir.Value, mbar_id: _ods_ir.Value[_ods_ir.IndexType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MBarrierGetOp(mbarrierPointer=mbarrier_pointer, barriers=barriers, mbarId=mbar_id, loc=loc, ip=ip).result

