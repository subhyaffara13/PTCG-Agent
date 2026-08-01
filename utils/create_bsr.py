
def create_bsr(spmat: _ods_ir.Type, async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], brows: _ods_ir.Value[_ods_ir.IndexType], bcols: _ods_ir.Value[_ods_ir.IndexType], bnnz: _ods_ir.Value[_ods_ir.IndexType], r_block_size: _ods_ir.Value[_ods_ir.IndexType], c_block_size: _ods_ir.Value[_ods_ir.IndexType], b_row_pos: _ods_ir.Value[_ods_ir.MemRefType], b_col_idxs: _ods_ir.Value[_ods_ir.MemRefType], values: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CreateBsrOp]:
  op = CreateBsrOp(spmat=spmat, asyncToken=async_token, asyncDependencies=async_dependencies, brows=brows, bcols=bcols, bnnz=bnnz, rBlockSize=r_block_size, cBlockSize=c_block_size, bRowPos=b_row_pos, bColIdxs=b_col_idxs, values=values, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

