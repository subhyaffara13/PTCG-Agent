
def named_computation(results_: _Sequence[_ods_ir.Type], tensors: _Sequence[_ods_ir.Value], origin: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, NamedComputationOp]:
  op = NamedComputationOp(results_=results_, tensors=tensors, origin=origin, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def named_computation(result: _Sequence[_ods_ir.Type], name: _Union[str, _ods_ir.StringAttr], operands_: _Sequence[_ods_ir.Value], *, in_shardings: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, out_shardings: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, NamedComputationOp]:
  op = NamedComputationOp(result=result, name=name, operands_=operands_, in_shardings=in_shardings, out_shardings=out_shardings, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

