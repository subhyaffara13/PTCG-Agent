
def fence(ordering: _Union[_Any, _ods_ir.Attribute], *, syncscope: _Optional[_Union[str, _ods_ir.StringAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> FenceOp:
  return FenceOp(ordering=ordering, syncscope=syncscope, loc=loc, ip=ip)

