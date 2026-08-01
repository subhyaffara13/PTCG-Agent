
def dynamic_reshape(result: _ods_ir.Type, operand: _ods_ir.Value, output_shape: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DynamicReshapeOp(result=result, operand=operand, output_shape=output_shape, loc=loc, ip=ip).result


def dynamic_reshape(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], output_shape: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicReshapeOp(result=result, operand=operand, output_shape=output_shape, loc=loc, ip=ip).result

