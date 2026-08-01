
def convert_bf16x2_to_f8x2(dst: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], dst_ty: _Union[_Any, _ods_ir.TypeAttr], *, rnd: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, sat: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConvertBF16x2ToF8x2Op(dst=dst, src=src, dstTy=dst_ty, rnd=rnd, sat=sat, relu=relu, loc=loc, ip=ip).result

