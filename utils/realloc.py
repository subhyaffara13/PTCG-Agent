
def realloc(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.MemRefType], *, dynamic_result_size: _Optional[_ods_ir.Value[_ods_ir.IndexType]] = None, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return ReallocOp(result=result, source=source, dynamicResultSize=dynamic_result_size, alignment=alignment, loc=loc, ip=ip).result

