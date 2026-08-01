
def va_arg(res: _ods_ir.Type, arg: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VaArgOp(res=res, arg=arg, loc=loc, ip=ip).result

