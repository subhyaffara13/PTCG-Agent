
def setmaxregister(reg_count: _Union[int, _ods_ir.IntegerAttr], action: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SetMaxRegisterOp:
  return SetMaxRegisterOp(regCount=reg_count, action=action, loc=loc, ip=ip)

