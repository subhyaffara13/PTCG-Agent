
def pack_subelements(output: _ods_ir.Type, sources: _Sequence[_ods_ir.Value[_ods_ir.VectorType]], positions: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], pack_format: _Union[_Any, _ods_ir.Attribute], *, unsigned_integers: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return PackSubelementsOp(output=output, sources=sources, positions=positions, pack_format=pack_format, unsigned_integers=unsigned_integers, loc=loc, ip=ip).result

