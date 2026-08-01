
def subgroup_mma_insert_thread_local(res: _ods_ir.Type, value: _ods_ir.Value, matrix: _ods_ir.Value, indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubgroupMmaInsertThreadLocalOp(res=res, value=value, matrix=matrix, indices=indices, loc=loc, ip=ip).result

