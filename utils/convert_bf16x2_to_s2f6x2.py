
def convert_bf16x2_to_s2f6x2(dst: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], *, scale_factor: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConvertBF16x2ToS2F6x2Op(dst=dst, src=src, scaleFactor=scale_factor, relu=relu, loc=loc, ip=ip).result

