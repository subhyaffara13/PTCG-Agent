
def descriptor_scatter(desc: _ods_ir.Value, x_offsets: _ods_ir.Value[_ods_ir.RankedTensorType], y_offset: _ods_ir.Value[_ods_ir.IntegerType], src: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DescriptorScatterOp:
  return DescriptorScatterOp(desc=desc, x_offsets=x_offsets, y_offset=y_offset, src=src, loc=loc, ip=ip)

