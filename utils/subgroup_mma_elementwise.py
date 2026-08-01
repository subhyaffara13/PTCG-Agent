
def subgroup_mma_elementwise(res: _ods_ir.Type, args: _Sequence[_ods_ir.Value], op_type: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubgroupMmaElementwiseOp(res=res, args=args, opType=op_type, loc=loc, ip=ip).result

