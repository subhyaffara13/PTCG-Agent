
def erase_memref_layout(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return EraseLayoutOp(result=result, operand=operand, loc=loc, ip=ip).result

