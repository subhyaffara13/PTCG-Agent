
def convert_float_to_tf32(src: _ods_ir.Value[_ods_ir.FloatType], *, rnd: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, sat: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return ConvertFloatToTF32Op(src=src, rnd=rnd, sat=sat, relu=relu, results=results, loc=loc, ip=ip).result

