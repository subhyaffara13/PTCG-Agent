
def descriptor_store(desc: _ods_ir.Value, src: _ods_ir.Value[_ods_ir.RankedTensorType], indices: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DescriptorStoreOp:
  return DescriptorStoreOp(desc=desc, src=src, indices=indices, loc=loc, ip=ip)

