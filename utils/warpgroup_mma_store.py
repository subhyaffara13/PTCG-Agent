
def warpgroup_mma_store(matrix_d: _ods_ir.Value, dst_memref: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> WarpgroupMmaStoreOp:
  return WarpgroupMmaStoreOp(matrixD=matrix_d, dstMemref=dst_memref, loc=loc, ip=ip)

