
def alloca(res: _ods_ir.Type, array_size: _ods_ir.Value[_ods_ir.IntegerType], elem_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, inalloca: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AllocaOp(res=res, arraySize=array_size, elem_type=elem_type, alignment=alignment, inalloca=inalloca, loc=loc, ip=ip).result


def alloca(memref: _ods_ir.Type, dynamic_sizes: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], symbol_operands: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return AllocaOp(memref=memref, dynamicSizes=dynamic_sizes, symbolOperands=symbol_operands, alignment=alignment, loc=loc, ip=ip).result

