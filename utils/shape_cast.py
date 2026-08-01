
def shape_cast(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ShapeCastOp(result=result, source=source, loc=loc, ip=ip).result

