
def sharding_group(input: _ods_ir.Value[_ods_ir.RankedTensorType], group_id: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ShardingGroupOp:
  return ShardingGroupOp(input=input, group_id=group_id, results=results, loc=loc, ip=ip)

