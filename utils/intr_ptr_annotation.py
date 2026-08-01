
def intr_ptr_annotation(ptr: _ods_ir.Value, annotation: _ods_ir.Value, file_name: _ods_ir.Value, line: _ods_ir.Value[_ods_ir.IntegerType], attr: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return PtrAnnotation(ptr=ptr, annotation=annotation, fileName=file_name, line=line, attr=attr, results=results, loc=loc, ip=ip).result

