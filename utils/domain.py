
def domain(operand: _ods_ir.Value, kind: _Union[_Any, _ods_ir.Attribute], entry_metadata: _Union[str, _ods_ir.StringAttr], exit_metadata: _Union[str, _ods_ir.StringAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DomainOp(operand=operand, kind=kind, entry_metadata=entry_metadata, exit_metadata=exit_metadata, results=results, loc=loc, ip=ip).result

