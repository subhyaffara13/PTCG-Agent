
def intr_annotation(integer: _ods_ir.Value[_ods_ir.IntegerType], annotation: _ods_ir.Value, file_name: _ods_ir.Value, line: _ods_ir.Value[_ods_ir.IntegerType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return Annotation(integer=integer, annotation=annotation, fileName=file_name, line=line, results=results, loc=loc, ip=ip).result

