
def convert_f8x2_to_f16x2(dst: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], src_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ConvertF8x2ToF16x2Op(dst=dst, src=src, srcType=src_type, relu=relu, loc=loc, ip=ip).result

