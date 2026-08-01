
def comdat(sym_name: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ComdatOp:
  return ComdatOp(sym_name=sym_name, loc=loc, ip=ip)

