
def subgroup_mma_extract_thread_local(matrix: _ods_ir.Value, indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubgroupMmaExtractThreadLocalOp(matrix=matrix, indices=indices, results=results, loc=loc, ip=ip).result

