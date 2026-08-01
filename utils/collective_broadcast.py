
def collective_broadcast(operand: _ods_ir.Value[_ods_ir.RankedTensorType], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CollectiveBroadcastOp(operand=operand, replica_groups=replica_groups, channel_handle=channel_handle, results=results, loc=loc, ip=ip).result


def collective_broadcast(operand: _ods_ir.Value[_ods_ir.RankedTensorType], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CollectiveBroadcastOp(operand=operand, replica_groups=replica_groups, channel_handle=channel_handle, results=results, loc=loc, ip=ip).result

