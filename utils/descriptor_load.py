
def descriptor_load(result: _ods_ir.Type, desc: _ods_ir.Value, indices: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, cache: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, evict: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DescriptorLoadOp(result=result, desc=desc, indices=indices, cache=cache, evict=evict, loc=loc, ip=ip).result

