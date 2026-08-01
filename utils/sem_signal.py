
def sem_signal(semaphore: _ods_ir.Value[_ods_ir.MemRefType], amount: _ods_ir.Value[_ods_ir.IntegerType], *, device_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, core_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, subcore_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SemaphoreSignalOp:
  return SemaphoreSignalOp(semaphore=semaphore, amount=amount, device_id=device_id, core_id=core_id, subcore_id=subcore_id, loc=loc, ip=ip)

