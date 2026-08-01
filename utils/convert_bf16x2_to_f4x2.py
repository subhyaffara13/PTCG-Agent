
def convert_bf16x2_to_f4x2(src: _ods_ir.Value[_ods_ir.VectorType], dst_ty: _Union[_Any, _ods_ir.TypeAttr], *, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return ConvertBF16x2ToF4x2Op(src=src, dstTy=dst_ty, relu=relu, results=results, loc=loc, ip=ip).result

