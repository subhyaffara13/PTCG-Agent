
def reduce_index(output: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.VectorType], axis: _Union[int, _ods_ir.IntegerAttr], kind: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ReduceIndexOp(output=output, input=input, axis=axis, kind=kind, loc=loc, ip=ip).result

