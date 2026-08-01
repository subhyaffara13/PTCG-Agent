
def dynamic_gather(source: _ods_ir.Value[_ods_ir.VectorType], indices: _ods_ir.Value[_ods_ir.VectorType], dimensions: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return DynamicGatherOp(source=source, indices=indices, dimensions=dimensions, results=results, loc=loc, ip=ip).result


def dynamic_gather(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _ods_ir.Value[_ods_ir.RankedTensorType], slice_sizes: _ods_ir.Value[_ods_ir.RankedTensorType], dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, indices_are_sorted: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicGatherOp(operand=operand, start_indices=start_indices, slice_sizes=slice_sizes, dimension_numbers=dimension_numbers, indices_are_sorted=indices_are_sorted, results=results, loc=loc, ip=ip).result


def dynamic_gather(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _ods_ir.Value[_ods_ir.RankedTensorType], slice_sizes: _ods_ir.Value[_ods_ir.RankedTensorType], dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, indices_are_sorted: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicGatherOp(operand=operand, start_indices=start_indices, slice_sizes=slice_sizes, dimension_numbers=dimension_numbers, indices_are_sorted=indices_are_sorted, results=results, loc=loc, ip=ip).result

