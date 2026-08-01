
def cp_async_bulk_shared_cluster_shared_cta(dst_mem: _ods_ir.Value, src_mem: _ods_ir.Value, mbar: _ods_ir.Value, size: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkSharedCTAToSharedClusterOp:
  return CpAsyncBulkSharedCTAToSharedClusterOp(dstMem=dst_mem, srcMem=src_mem, mbar=mbar, size=size, loc=loc, ip=ip)

