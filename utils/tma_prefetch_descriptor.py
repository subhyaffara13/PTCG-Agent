
def tma_prefetch_descriptor(tensor_map_descriptor: _ods_ir.Value, *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TmaPrefetchOp:
  return TmaPrefetchOp(tensorMapDescriptor=tensor_map_descriptor, predicate=predicate, loc=loc, ip=ip)

