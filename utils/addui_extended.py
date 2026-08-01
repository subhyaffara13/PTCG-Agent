
def addui_extended(sum: _ods_ir.Type, overflow: _ods_ir.Type, lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return AddUIExtendedOp(sum=sum, overflow=overflow, lhs=lhs, rhs=rhs, loc=loc, ip=ip).results

