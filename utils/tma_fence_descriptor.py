
def tma_fence_descriptor(tensor_map_descriptor: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TmaFenceOp:
  return TmaFenceOp(tensorMapDescriptor=tensor_map_descriptor, loc=loc, ip=ip)

