
def subgroup_mma_compute(op_a: _ods_ir.Value, op_b: _ods_ir.Value, op_c: _ods_ir.Value, *, a_transpose: _Optional[bool] = None, b_transpose: _Optional[bool] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubgroupMmaComputeOp(opA=op_a, opB=op_b, opC=op_c, a_transpose=a_transpose, b_transpose=b_transpose, results=results, loc=loc, ip=ip).result

