
def convert_f32x4_to_f4x4(src: _ods_ir.Value[_ods_ir.VectorType], rbits: _ods_ir.Value[_ods_ir.IntegerType], dst_ty: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return ConvertF32x4ToF4x4Op(src=src, rbits=rbits, dstTy=dst_ty, relu=relu, results=results, loc=loc, ip=ip).result

