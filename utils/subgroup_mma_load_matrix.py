
def subgroup_mma_load_matrix(res: _ods_ir.Type, src_memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], lead_dimension: _Union[int, _ods_ir.IntegerAttr], *, transpose: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubgroupMmaLoadMatrixOp(res=res, srcMemref=src_memref, indices=indices, leadDimension=lead_dimension, transpose=transpose, loc=loc, ip=ip).result

