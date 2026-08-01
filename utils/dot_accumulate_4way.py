
def dot_accumulate_4way(a: _ods_ir.Value[_ods_ir.VectorType], a_type: _Union[_Any, _ods_ir.Attribute], b: _ods_ir.Value[_ods_ir.VectorType], b_type: _Union[_Any, _ods_ir.Attribute], c: _ods_ir.Value[_ods_ir.IntegerType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return DotAccumulate4WayOp(a=a, a_type=a_type, b=b, b_type=b_type, c=c, results=results, loc=loc, ip=ip).result

