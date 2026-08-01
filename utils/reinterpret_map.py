
def reinterpret_map(dest: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReinterpretMapOp(dest=dest, source=source, loc=loc, ip=ip).result

