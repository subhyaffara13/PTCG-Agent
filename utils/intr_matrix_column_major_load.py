
def intr_matrix_column_major_load(res: _ods_ir.Type, data: _ods_ir.Value, stride: _ods_ir.Value[_ods_ir.IntegerType], is_volatile: _Union[bool, _ods_ir.BoolAttr], rows: _Union[int, _ods_ir.IntegerAttr], columns: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MatrixColumnMajorLoadOp(res=res, data=data, stride=stride, isVolatile=is_volatile, rows=rows, columns=columns, loc=loc, ip=ip).result

