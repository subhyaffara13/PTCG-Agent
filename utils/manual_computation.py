
def manual_computation(results_: _Sequence[_ods_ir.Type], tensors: _Sequence[_ods_ir.Value], in_shardings: _Union[_Any, _ods_ir.Attribute], out_shardings: _Union[_Any, _ods_ir.Attribute], manual_axes: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ManualComputationOp]:
  op = ManualComputationOp(results_=results_, tensors=tensors, in_shardings=in_shardings, out_shardings=out_shardings, manual_axes=manual_axes, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

