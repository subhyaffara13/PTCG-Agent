
def sem_alloc(result: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return AllocaSemaphoreOp(result=result, loc=loc, ip=ip).result

