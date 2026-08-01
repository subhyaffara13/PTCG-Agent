
def sem_barrier(semaphore: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return GetBarrierSemaphoreOp(semaphore=semaphore, loc=loc, ip=ip).result

