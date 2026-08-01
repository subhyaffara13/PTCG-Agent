
def torch_index_select(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], index: _ods_ir.Value[_ods_ir.RankedTensorType], dim: _Union[int, _ods_ir.IntegerAttr], batch_dims: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TorchIndexSelectOp(result=result, operand=operand, index=index, dim=dim, batch_dims=batch_dims, loc=loc, ip=ip).result


def torch_index_select(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], index: _ods_ir.Value[_ods_ir.RankedTensorType], dim: _Union[int, _ods_ir.IntegerAttr], batch_dims: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TorchIndexSelectOp(result=result, operand=operand, index=index, dim=dim, batch_dims=batch_dims, loc=loc, ip=ip).result

