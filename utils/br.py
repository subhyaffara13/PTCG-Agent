
def br(dest_operands: _Sequence[_ods_ir.Value], dest: _ods_ir.Block, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BranchOp:
  return BranchOp(destOperands=dest_operands, dest=dest, loc=loc, ip=ip)


def br(dest_operands: _Sequence[_ods_ir.Value], dest: _ods_ir.Block, *, loop_annotation: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BrOp:
  return BrOp(destOperands=dest_operands, dest=dest, loop_annotation=loop_annotation, loc=loc, ip=ip)

