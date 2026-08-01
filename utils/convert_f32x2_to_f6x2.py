
def convert_f32x2_to_f6x2(dst: _ods_ir.Type, a: _ods_ir.Value[_ods_ir.FloatType], b: _ods_ir.Value[_ods_ir.FloatType], dst_ty: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConvertF32x2ToF6x2Op(dst=dst, a=a, b=b, dstTy=dst_ty, relu=relu, loc=loc, ip=ip).result

