
def make_tensor_descriptor(result: _ods_ir.Type, base: _ods_ir.Value, shape: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], strides: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, padding: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MakeTensorDescOp(result=result, base=base, shape=shape, strides=strides, padding=padding, loc=loc, ip=ip).result

