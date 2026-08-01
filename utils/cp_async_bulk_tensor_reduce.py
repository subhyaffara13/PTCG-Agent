
def cp_async_bulk_tensor_reduce(tma_descriptor: _ods_ir.Value, src_mem: _ods_ir.Value, red_kind: _Union[_Any, _ods_ir.Attribute], coordinates: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, mode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, l2_cache_hint: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkTensorReduceOp:
  return CpAsyncBulkTensorReduceOp(tmaDescriptor=tma_descriptor, srcMem=src_mem, redKind=red_kind, coordinates=coordinates, mode=mode, l2CacheHint=l2_cache_hint, loc=loc, ip=ip)

