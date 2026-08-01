
def subgroup_broadcast(src: _ods_ir.Value, broadcast_type: _Union[_Any, _ods_ir.Attribute], *, lane: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubgroupBroadcastOp(src=src, broadcast_type=broadcast_type, lane=lane, results=results, loc=loc, ip=ip).result

