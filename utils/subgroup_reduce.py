
def subgroup_reduce(value: _ods_ir.Value, op: _Union[_Any, _ods_ir.Attribute], *, uniform: _Optional[bool] = None, cluster_size: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, cluster_stride: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubgroupReduceOp(value=value, op=op, uniform=uniform, cluster_size=cluster_size, cluster_stride=cluster_stride, results=results, loc=loc, ip=ip).result

