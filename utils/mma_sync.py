
def mma_sync(res: _ods_ir.Type, matrix_a: _ods_ir.Value[_ods_ir.VectorType], matrix_b: _ods_ir.Value[_ods_ir.VectorType], matrix_c: _ods_ir.Value[_ods_ir.VectorType], mma_shape: _Union[_Sequence[int], _ods_ir.ArrayAttr], *, tf32_enabled: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MmaSyncOp(res=res, matrixA=matrix_a, matrixB=matrix_b, matrixC=matrix_c, mmaShape=mma_shape, tf32Enabled=tf32_enabled, loc=loc, ip=ip).result


def mma_sync(res: _ods_ir.Type, shape: _Union[_Any, _ods_ir.Attribute], layout_a: _Union[_Any, _ods_ir.Attribute], layout_b: _Union[_Any, _ods_ir.Attribute], operand_a: _Sequence[_ods_ir.Value], operand_b: _Sequence[_ods_ir.Value], operand_c: _Sequence[_ods_ir.Value], *, b1_op: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, int_overflow_behavior: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, multiplicand_a_ptx_type: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, multiplicand_b_ptx_type: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MmaOp(res=res, shape=shape, layoutA=layout_a, layoutB=layout_b, operandA=operand_a, operandB=operand_b, operandC=operand_c, b1Op=b1_op, intOverflowBehavior=int_overflow_behavior, multiplicandAPtxType=multiplicand_a_ptx_type, multiplicandBPtxType=multiplicand_b_ptx_type, loc=loc, ip=ip).result

