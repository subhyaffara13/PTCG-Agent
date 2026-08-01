
def minimum_broadcast_shapes(results_: _Sequence[_ods_ir.Type], shapes: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, MinimumBroadcastShapesOp]:
  op = MinimumBroadcastShapesOp(results_=results_, shapes=shapes, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

