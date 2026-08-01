
def subui_extended(diff: _ods_ir.Type, borrow: _ods_ir.Type, lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return SubUIExtendedOp(diff=diff, borrow=borrow, lhs=lhs, rhs=rhs, loc=loc, ip=ip).results

