
def descriptor_gather(result: _ods_ir.Type, desc: _ods_ir.Value, x_offsets: _ods_ir.Value[_ods_ir.RankedTensorType], y_offset: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DescriptorGatherOp(result=result, desc=desc, x_offsets=x_offsets, y_offset=y_offset, loc=loc, ip=ip).result

