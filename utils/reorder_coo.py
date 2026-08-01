
def reorder_coo(result_coo: _ods_ir.Type, input_coo: _ods_ir.Value[_ods_ir.RankedTensorType], algorithm: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReorderCOOOp(result_coo=result_coo, input_coo=input_coo, algorithm=algorithm, loc=loc, ip=ip).result

