
def comdat_selector(sym_name: _Union[str, _ods_ir.StringAttr], comdat: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ComdatSelectorOp:
  return ComdatSelectorOp(sym_name=sym_name, comdat=comdat, loc=loc, ip=ip)

