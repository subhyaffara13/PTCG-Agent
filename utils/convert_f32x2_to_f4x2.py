
def convert_f32x2_to_f4x2(a: _ods_ir.Value[_ods_ir.FloatType], b: _ods_ir.Value[_ods_ir.FloatType], dst_ty: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return ConvertF32x2ToF4x2Op(a=a, b=b, dstTy=dst_ty, relu=relu, results=results, loc=loc, ip=ip).result

