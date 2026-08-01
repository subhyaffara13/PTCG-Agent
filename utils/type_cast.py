
def type_cast(result: _ods_ir.Type, memref: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return TypeCastOp(result=result, memref=memref, loc=loc, ip=ip).result

