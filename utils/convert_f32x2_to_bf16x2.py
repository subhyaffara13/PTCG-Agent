
def convert_f32x2_to_bf16x2(dst: _ods_ir.Type, src_hi: _ods_ir.Value[_ods_ir.FloatType], src_lo: _ods_ir.Value[_ods_ir.FloatType], *, random_bits: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, rnd: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, sat: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ConvertF32x2ToBF16x2Op(dst=dst, src_hi=src_hi, src_lo=src_lo, random_bits=random_bits, rnd=rnd, sat=sat, relu=relu, loc=loc, ip=ip).result

