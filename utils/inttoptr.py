
def inttoptr(res: _ods_ir.Type, arg: _ods_ir.Value, *, dereferenceable: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IntToPtrOp(res=res, arg=arg, dereferenceable=dereferenceable, loc=loc, ip=ip).result

