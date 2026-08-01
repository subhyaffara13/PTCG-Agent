
def tma_create_descriptor(tensor_map: _ods_ir.Type, tensor: _ods_ir.Value[_ods_ir.UnrankedMemRefType], box_dimensions: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TmaCreateDescriptorOp(tensorMap=tensor_map, tensor=tensor, boxDimensions=box_dimensions, loc=loc, ip=ip).result

