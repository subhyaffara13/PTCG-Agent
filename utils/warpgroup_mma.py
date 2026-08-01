
def warpgroup_mma(matrix_d: _ods_ir.Type, descriptor_a: _ods_ir.Value, descriptor_b: _ods_ir.Value, matrix_c: _ods_ir.Value, *, wait_group: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, transpose_a: _Optional[bool] = None, transpose_b: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return WarpgroupMmaOp(matrixD=matrix_d, descriptorA=descriptor_a, descriptorB=descriptor_b, matrixC=matrix_c, waitGroup=wait_group, transposeA=transpose_a, transposeB=transpose_b, loc=loc, ip=ip).result

