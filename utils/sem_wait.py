
def sem_wait(semaphore: _ods_ir.Value[_ods_ir.MemRefType], amount: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SemaphoreWaitOp:
  return SemaphoreWaitOp(semaphore=semaphore, amount=amount, loc=loc, ip=ip)

