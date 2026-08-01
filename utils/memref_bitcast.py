
def memref_bitcast(result: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return MemRefBitcastOp(result=result, input=input, loc=loc, ip=ip).result

