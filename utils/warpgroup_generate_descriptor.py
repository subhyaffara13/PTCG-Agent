
def warpgroup_generate_descriptor(descriptor: _ods_ir.Type, tensor: _ods_ir.Value[_ods_ir.MemRefType], tensor_map: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return WarpgroupGenerateDescriptorOp(descriptor=descriptor, tensor=tensor, tensorMap=tensor_map, loc=loc, ip=ip).result

