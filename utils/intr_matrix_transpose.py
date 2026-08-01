
def intr_matrix_transpose(res: _ods_ir.Type, matrix: _ods_ir.Value[_ods_ir.VectorType], rows: _Union[int, _ods_ir.IntegerAttr], columns: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MatrixTransposeOp(res=res, matrix=matrix, rows=rows, columns=columns, loc=loc, ip=ip).result

