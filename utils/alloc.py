
def alloc(memref: _ods_ir.Type, async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], dynamic_sizes: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], symbol_operands: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, host_shared: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, AllocOp]:
  op = AllocOp(memref=memref, asyncToken=async_token, asyncDependencies=async_dependencies, dynamicSizes=dynamic_sizes, symbolOperands=symbol_operands, hostShared=host_shared, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def alloc(memref: _ods_ir.Type, dynamic_sizes: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], symbol_operands: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return AllocOp(memref=memref, dynamicSizes=dynamic_sizes, symbolOperands=symbol_operands, alignment=alignment, loc=loc, ip=ip).result

