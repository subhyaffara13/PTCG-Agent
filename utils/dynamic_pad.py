
def dynamic_pad(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], padding_value: _ods_ir.Value[_ods_ir.RankedTensorType], edge_padding_low: _ods_ir.Value[_ods_ir.RankedTensorType], edge_padding_high: _ods_ir.Value[_ods_ir.RankedTensorType], interior_padding: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicPadOp(result=result, operand=operand, padding_value=padding_value, edge_padding_low=edge_padding_low, edge_padding_high=edge_padding_high, interior_padding=interior_padding, loc=loc, ip=ip).result


def dynamic_pad(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], padding_value: _ods_ir.Value[_ods_ir.RankedTensorType], edge_padding_low: _ods_ir.Value[_ods_ir.RankedTensorType], edge_padding_high: _ods_ir.Value[_ods_ir.RankedTensorType], interior_padding: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicPadOp(result=result, operand=operand, padding_value=padding_value, edge_padding_low=edge_padding_low, edge_padding_high=edge_padding_high, interior_padding=interior_padding, loc=loc, ip=ip).result

