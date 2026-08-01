
def intr_matrix_column_major_store(matrix: _ods_ir.Value[_ods_ir.VectorType], data: _ods_ir.Value, stride: _ods_ir.Value[_ods_ir.IntegerType], is_volatile: _Union[bool, _ods_ir.BoolAttr], rows: _Union[int, _ods_ir.IntegerAttr], columns: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MatrixColumnMajorStoreOp:
  return MatrixColumnMajorStoreOp(matrix=matrix, data=data, stride=stride, isVolatile=is_volatile, rows=rows, columns=columns, loc=loc, ip=ip)

