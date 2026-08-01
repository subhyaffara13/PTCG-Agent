
def cross_replica_sum(operand: _ods_ir.Value[_ods_ir.RankedTensorType], replica_groups: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CrossReplicaSumOp(operand=operand, replica_groups=replica_groups, results=results, loc=loc, ip=ip).result


def cross_replica_sum(operand: _ods_ir.Value[_ods_ir.RankedTensorType], replica_groups: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CrossReplicaSumOp(operand=operand, replica_groups=replica_groups, results=results, loc=loc, ip=ip).result

