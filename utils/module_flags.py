
def module_flags(flags: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ModuleFlagsOp:
  return ModuleFlagsOp(flags=flags, loc=loc, ip=ip)

