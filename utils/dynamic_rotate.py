
def dynamic_rotate(value: _ods_ir.Value[_ods_ir.VectorType], amount: _ods_ir.Value[_ods_ir.IntegerType], dimension: _Union[int, _ods_ir.IntegerAttr], *, stride: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, stride_dimension: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return DynamicRotateOp(value=value, amount=amount, dimension=dimension, stride=stride, stride_dimension=stride_dimension, results=results, loc=loc, ip=ip).result

