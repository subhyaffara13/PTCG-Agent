
def create_coo_aos(spmat: _ods_ir.Type, async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], rows: _ods_ir.Value[_ods_ir.IndexType], cols: _ods_ir.Value[_ods_ir.IndexType], nnz: _ods_ir.Value[_ods_ir.IndexType], idxs: _ods_ir.Value[_ods_ir.MemRefType], values: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CreateCooAoSOp]:
  op = CreateCooAoSOp(spmat=spmat, asyncToken=async_token, asyncDependencies=async_dependencies, rows=rows, cols=cols, nnz=nnz, idxs=idxs, values=values, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

