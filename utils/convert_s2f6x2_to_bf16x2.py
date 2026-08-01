
def convert_s2f6x2_to_bf16x2(dst: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], *, scale_factor: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, sat: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ConvertS2F6x2ToBF16x2Op(dst=dst, src=src, scaleFactor=scale_factor, sat=sat, relu=relu, loc=loc, ip=ip).result

