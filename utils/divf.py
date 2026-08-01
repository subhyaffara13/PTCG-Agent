
def divf(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, roundingmode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DivFOp(lhs=lhs, rhs=rhs, fastmath=fastmath, roundingmode=roundingmode, results=results, loc=loc, ip=ip).result


def divf(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, rnd: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, approx: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, full: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DivFOp(lhs=lhs, rhs=rhs, rnd=rnd, ftz=ftz, approx=approx, full=full, results=results, loc=loc, ip=ip).result

