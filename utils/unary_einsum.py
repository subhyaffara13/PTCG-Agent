
def unary_einsum(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], einsum_config: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return UnaryEinsumOp(result=result, operand=operand, einsum_config=einsum_config, loc=loc, ip=ip).result

