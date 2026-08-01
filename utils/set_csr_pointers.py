
def set_csr_pointers(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], spmat: _ods_ir.Value, positions: _ods_ir.Value[_ods_ir.MemRefType], coordinates: _ods_ir.Value[_ods_ir.MemRefType], values: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, SetCsrPointersOp]:
  op = SetCsrPointersOp(asyncToken=async_token, asyncDependencies=async_dependencies, spmat=spmat, positions=positions, coordinates=coordinates, values=values, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

