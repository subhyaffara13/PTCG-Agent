
def set_dimension_size(operand: _ods_ir.Value[_ods_ir.RankedTensorType], size: _ods_ir.Value, dimension: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SetDimensionSizeOp(operand=operand, size=size, dimension=dimension, results=results, loc=loc, ip=ip).result


def set_dimension_size(operand: _ods_ir.Value[_ods_ir.RankedTensorType], size: _ods_ir.Value[_ods_ir.RankedTensorType], dimension: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SetDimensionSizeOp(operand=operand, size=size, dimension=dimension, results=results, loc=loc, ip=ip).result

