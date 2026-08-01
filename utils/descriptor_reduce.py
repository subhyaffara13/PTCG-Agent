
def descriptor_reduce(kind: _Union[_Any, _ods_ir.Attribute], desc: _ods_ir.Value, src: _ods_ir.Value[_ods_ir.RankedTensorType], indices: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DescriptorReduceOp:
  return DescriptorReduceOp(kind=kind, desc=desc, src=src, indices=indices, loc=loc, ip=ip)

