
def collective_permute(operand: _ods_ir.Value[_ods_ir.RankedTensorType], source_target_pairs: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CollectivePermuteOp(operand=operand, source_target_pairs=source_target_pairs, channel_handle=channel_handle, results=results, loc=loc, ip=ip).result


def collective_permute(tensor: _ods_ir.Value, out_sharding: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CollectivePermuteOp(tensor=tensor, out_sharding=out_sharding, results=results, loc=loc, ip=ip).result


def collective_permute(operand: _ods_ir.Value[_ods_ir.RankedTensorType], source_target_pairs: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CollectivePermuteOp(operand=operand, source_target_pairs=source_target_pairs, channel_handle=channel_handle, results=results, loc=loc, ip=ip).result

