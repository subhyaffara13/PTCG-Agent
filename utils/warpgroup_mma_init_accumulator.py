
def warpgroup_mma_init_accumulator(matrix_c: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return WarpgroupMmaInitAccumulatorOp(matrixC=matrix_c, loc=loc, ip=ip).result

