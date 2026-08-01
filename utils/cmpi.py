
def cmpi(predicate: _Union[_Any, _ods_ir.Attribute], lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CmpIOp(predicate=predicate, lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result

