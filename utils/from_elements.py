
def from_elements(dest: _ods_ir.Type, elements: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return FromElementsOp(dest=dest, elements=elements, loc=loc, ip=ip).result

