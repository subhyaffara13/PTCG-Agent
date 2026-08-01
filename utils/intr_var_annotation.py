
def intr_var_annotation(val: _ods_ir.Value, annotation: _ods_ir.Value, file_name: _ods_ir.Value, line: _ods_ir.Value[_ods_ir.IntegerType], attr: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> VarAnnotation:
  return VarAnnotation(val=val, annotation=annotation, fileName=file_name, line=line, attr=attr, loc=loc, ip=ip)

