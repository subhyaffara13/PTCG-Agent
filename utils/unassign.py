
def unassign(tensor: _ods_ir.Value, *, origin: _Optional[_Union[str, _ods_ir.StringAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return UnassignOp(tensor=tensor, origin=origin, results=results, loc=loc, ip=ip).result

