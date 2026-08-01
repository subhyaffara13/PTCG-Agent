
def convert_f32x2_to_s2f6x2(dst: _ods_ir.Type, a: _ods_ir.Value[_ods_ir.FloatType], b: _ods_ir.Value[_ods_ir.FloatType], *, scale_factor: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConvertF32x2ToS2F6x2Op(dst=dst, a=a, b=b, scaleFactor=scale_factor, relu=relu, loc=loc, ip=ip).result

