
def unpack_subelements(output: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], index: _Union[int, _ods_ir.IntegerAttr], pack_format: _Union[_Any, _ods_ir.Attribute], *, integer_extended: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, unsigned_integers: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return UnpackSubelementsOp(output=output, source=source, index=index, pack_format=pack_format, integer_extended=integer_extended, unsigned_integers=unsigned_integers, loc=loc, ip=ip).result

