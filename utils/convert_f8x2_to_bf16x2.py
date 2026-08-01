
def convert_f8x2_to_bf16x2(dst: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], src_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ConvertF8x2ToBF16x2Op(dst=dst, src=src, srcType=src_type, loc=loc, ip=ip).result

