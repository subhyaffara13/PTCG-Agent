
def spmat_get_size(rows: _ods_ir.Type, cols: _ods_ir.Type, nnz: _ods_ir.Type, async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], spmat: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, SpMatGetSizeOp]:
  op = SpMatGetSizeOp(rows=rows, cols=cols, nnz=nnz, asyncToken=async_token, asyncDependencies=async_dependencies, spmat=spmat, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

