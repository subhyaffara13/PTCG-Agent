
def barrier_reduction(reduction_op: _Union[_Any, _ods_ir.Attribute], reduction_predicate: _ods_ir.Value[_ods_ir.IntegerType], *, barrier_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return BarrierReductionOp(reductionOp=reduction_op, reductionPredicate=reduction_predicate, barrierId=barrier_id, results=results, loc=loc, ip=ip).result

