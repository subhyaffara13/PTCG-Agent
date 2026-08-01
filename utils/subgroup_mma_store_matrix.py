
def subgroup_mma_store_matrix(src: _ods_ir.Value, dst_memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], lead_dimension: _Union[int, _ods_ir.IntegerAttr], *, transpose: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SubgroupMmaStoreMatrixOp:
  return SubgroupMmaStoreMatrixOp(src=src, dstMemref=dst_memref, indices=indices, leadDimension=lead_dimension, transpose=transpose, loc=loc, ip=ip)

