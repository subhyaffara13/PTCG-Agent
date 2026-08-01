
def cp_async_bulk_prefetch(src_mem: _ods_ir.Value, size: _ods_ir.Value[_ods_ir.IntegerType], *, l2_cache_hint: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkPrefetchOp:
  return CpAsyncBulkPrefetchOp(srcMem=src_mem, size=size, l2CacheHint=l2_cache_hint, loc=loc, ip=ip)

