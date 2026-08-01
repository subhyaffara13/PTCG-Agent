
def cond_br(condition: _ods_ir.Value[_ods_ir.IntegerType], true_dest_operands: _Sequence[_ods_ir.Value], false_dest_operands: _Sequence[_ods_ir.Value], true_dest: _ods_ir.Block, false_dest: _ods_ir.Block, *, branch_weights: _Optional[_Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CondBranchOp:
  return CondBranchOp(condition=condition, trueDestOperands=true_dest_operands, falseDestOperands=false_dest_operands, trueDest=true_dest, falseDest=false_dest, branch_weights=branch_weights, loc=loc, ip=ip)


def cond_br(condition: _ods_ir.Value[_ods_ir.IntegerType], true_dest_operands: _Sequence[_ods_ir.Value], false_dest_operands: _Sequence[_ods_ir.Value], true_dest: _ods_ir.Block, false_dest: _ods_ir.Block, *, branch_weights: _Optional[_Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr]] = None, loop_annotation: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CondBrOp:
  return CondBrOp(condition=condition, trueDestOperands=true_dest_operands, falseDestOperands=false_dest_operands, trueDest=true_dest, falseDest=false_dest, branch_weights=branch_weights, loop_annotation=loop_annotation, loc=loc, ip=ip)

