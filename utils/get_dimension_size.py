
def get_dimension_size(operand: _ods_ir.Value[_ods_ir.RankedTensorType], dimension: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return GetDimensionSizeOp(operand=operand, dimension=dimension, results=results, loc=loc, ip=ip).result


def get_dimension_size(operand: _ods_ir.Value[_ods_ir.RankedTensorType], dimension: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return GetDimensionSizeOp(operand=operand, dimension=dimension, results=results, loc=loc, ip=ip).result

