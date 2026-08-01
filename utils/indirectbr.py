
def indirectbr(addr: _ods_ir.Value, succ_operands: _Sequence[_ods_ir.Value], indbr_operand_segments: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], successors: _Sequence[_ods_ir.Block], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> IndirectBrOp:
  return IndirectBrOp(addr=addr, succOperands=succ_operands, indbr_operand_segments=indbr_operand_segments, successors=successors, loc=loc, ip=ip)

