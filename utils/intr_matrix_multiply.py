
def intr_matrix_multiply(res: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.VectorType], rhs: _ods_ir.Value[_ods_ir.VectorType], lhs_rows: _Union[int, _ods_ir.IntegerAttr], lhs_columns: _Union[int, _ods_ir.IntegerAttr], rhs_columns: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MatrixMultiplyOp(res=res, lhs=lhs, rhs=rhs, lhs_rows=lhs_rows, lhs_columns=lhs_columns, rhs_columns=rhs_columns, loc=loc, ip=ip).result

