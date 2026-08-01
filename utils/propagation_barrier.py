
def propagation_barrier(input: _ods_ir.Value[_ods_ir.RankedTensorType], allowed_direction: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return PropagationBarrierOp(input=input, allowed_direction=allowed_direction, results=results, loc=loc, ip=ip).result

