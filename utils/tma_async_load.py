
def tma_async_load(dst: _ods_ir.Value[_ods_ir.MemRefType], barriers: _ods_ir.Value, tensor_map_descriptor: _ods_ir.Value, coordinates: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], mbar_id: _ods_ir.Value[_ods_ir.IndexType], *, multicast_mask: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TmaAsyncLoadOp:
  return TmaAsyncLoadOp(dst=dst, barriers=barriers, tensorMapDescriptor=tensor_map_descriptor, coordinates=coordinates, mbarId=mbar_id, multicastMask=multicast_mask, predicate=predicate, loc=loc, ip=ip)

