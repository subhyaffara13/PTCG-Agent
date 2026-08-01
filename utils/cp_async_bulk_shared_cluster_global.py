
def cp_async_bulk_shared_cluster_global(dst_mem: _ods_ir.Value, src_mem: _ods_ir.Value, mbar: _ods_ir.Value, size: _ods_ir.Value[_ods_ir.IntegerType], *, multicast_mask: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, l2_cache_hint: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkGlobalToSharedClusterOp:
  return CpAsyncBulkGlobalToSharedClusterOp(dstMem=dst_mem, srcMem=src_mem, mbar=mbar, size=size, multicastMask=multicast_mask, l2CacheHint=l2_cache_hint, loc=loc, ip=ip)

