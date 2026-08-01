
def dealloc(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], memref: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, DeallocOp]:
  op = DeallocOp(asyncToken=async_token, asyncDependencies=async_dependencies, memref=memref, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def dealloc(memref: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DeallocOp:
  return DeallocOp(memref=memref, loc=loc, ip=ip)

