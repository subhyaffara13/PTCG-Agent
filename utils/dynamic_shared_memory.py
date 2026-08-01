
def dynamic_shared_memory(result_memref: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return DynamicSharedMemoryOp(resultMemref=result_memref, loc=loc, ip=ip).result

