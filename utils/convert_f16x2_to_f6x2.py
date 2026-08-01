
def convert_f16x2_to_f6x2(dst: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], dst_ty: _Union[_Any, _ods_ir.TypeAttr], *, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConvertF16x2ToF6x2Op(dst=dst, src=src, dstTy=dst_ty, relu=relu, loc=loc, ip=ip).result

