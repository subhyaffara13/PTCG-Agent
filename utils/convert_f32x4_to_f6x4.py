
def convert_f32x4_to_f6x4(dst: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], rbits: _ods_ir.Value[_ods_ir.IntegerType], dst_ty: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ConvertF32x4ToF6x4Op(dst=dst, src=src, rbits=rbits, dstTy=dst_ty, relu=relu, loc=loc, ip=ip).result

