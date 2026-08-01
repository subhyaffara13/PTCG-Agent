
def tma_async_store(src: _ods_ir.Value[_ods_ir.MemRefType], tensor_map_descriptor: _ods_ir.Value, coordinates: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TmaAsyncStoreOp:
  return TmaAsyncStoreOp(src=src, tensorMapDescriptor=tensor_map_descriptor, coordinates=coordinates, predicate=predicate, loc=loc, ip=ip)

