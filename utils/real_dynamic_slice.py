
def real_dynamic_slice(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _ods_ir.Value[_ods_ir.RankedTensorType], limit_indices: _ods_ir.Value[_ods_ir.RankedTensorType], strides: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RealDynamicSliceOp(result=result, operand=operand, start_indices=start_indices, limit_indices=limit_indices, strides=strides, loc=loc, ip=ip).result


def real_dynamic_slice(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _ods_ir.Value[_ods_ir.RankedTensorType], limit_indices: _ods_ir.Value[_ods_ir.RankedTensorType], strides: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RealDynamicSliceOp(result=result, operand=operand, start_indices=start_indices, limit_indices=limit_indices, strides=strides, loc=loc, ip=ip).result

