
def cp_async_bulk_tensor_global_shared_cta(tma_descriptor: _ods_ir.Value, src_mem: _ods_ir.Value, coordinates: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, l2_cache_hint: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, mode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkTensorSharedCTAToGlobalOp:
  return CpAsyncBulkTensorSharedCTAToGlobalOp(tmaDescriptor=tma_descriptor, srcMem=src_mem, coordinates=coordinates, l2CacheHint=l2_cache_hint, mode=mode, predicate=predicate, loc=loc, ip=ip)

