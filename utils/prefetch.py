
def prefetch(memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], is_write: _Union[bool, _ods_ir.BoolAttr], locality_hint: _Union[int, _ods_ir.IntegerAttr], is_data_cache: _Union[bool, _ods_ir.BoolAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PrefetchOp:
  return PrefetchOp(memref=memref, indices=indices, isWrite=is_write, localityHint=locality_hint, isDataCache=is_data_cache, loc=loc, ip=ip)


def prefetch(addr: _ods_ir.Value, *, cache_level: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, evict_priority: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, tensormap: _Optional[bool] = None, uniform: _Optional[bool] = None, in_param_space: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PrefetchOp:
  return PrefetchOp(addr=addr, cacheLevel=cache_level, evictPriority=evict_priority, predicate=predicate, tensormap=tensormap, uniform=uniform, in_param_space=in_param_space, loc=loc, ip=ip)

