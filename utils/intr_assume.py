
def intr_assume(cond: _ods_ir.Value[_ods_ir.IntegerType], op_bundle_operands: _Sequence[_ods_ir.Value], op_bundle_sizes: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, op_bundle_tags: _Optional[_Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> AssumeOp:
  return AssumeOp(cond=cond, op_bundle_operands=op_bundle_operands, op_bundle_sizes=op_bundle_sizes, op_bundle_tags=op_bundle_tags, loc=loc, ip=ip)

