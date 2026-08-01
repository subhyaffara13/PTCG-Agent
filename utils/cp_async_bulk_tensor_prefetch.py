
def cp_async_bulk_tensor_prefetch(tma_descriptor: _ods_ir.Value, coordinates: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], im2col_offsets: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, mode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, l2_cache_hint: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkTensorPrefetchOp:
  return CpAsyncBulkTensorPrefetchOp(tmaDescriptor=tma_descriptor, coordinates=coordinates, im2colOffsets=im2col_offsets, mode=mode, l2CacheHint=l2_cache_hint, loc=loc, ip=ip)

