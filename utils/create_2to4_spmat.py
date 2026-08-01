
def create_2to4_spmat(sp_mat: _ods_ir.Type, async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], rows: _ods_ir.Value[_ods_ir.IndexType], cols: _ods_ir.Value[_ods_ir.IndexType], memref: _ods_ir.Value[_ods_ir.MemRefType], *, prune_flag: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, Create2To4SpMatOp]:
  op = Create2To4SpMatOp(spMat=sp_mat, asyncToken=async_token, asyncDependencies=async_dependencies, rows=rows, cols=cols, memref=memref, pruneFlag=prune_flag, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

