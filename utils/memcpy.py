
def memcpy(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], dst: _ods_ir.Value[_ods_ir.MemRefType], src: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, MemcpyOp]:
  op = MemcpyOp(asyncToken=async_token, asyncDependencies=async_dependencies, dst=dst, src=src, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

