
def generic_atomic_rmw(result: _ods_ir.Type, memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return GenericAtomicRMWOp(result=result, memref=memref, indices=indices, loc=loc, ip=ip).result

