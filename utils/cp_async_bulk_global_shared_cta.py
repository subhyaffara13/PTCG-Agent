
def cp_async_bulk_global_shared_cta(dst_mem: _ods_ir.Value, src_mem: _ods_ir.Value, size: _ods_ir.Value[_ods_ir.IntegerType], *, l2_cache_hint: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, byte_mask: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkSharedCTAToGlobalOp:
  return CpAsyncBulkSharedCTAToGlobalOp(dstMem=dst_mem, srcMem=src_mem, size=size, l2CacheHint=l2_cache_hint, byteMask=byte_mask, loc=loc, ip=ip)

