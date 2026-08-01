
def linker_options(options: _Union[_Sequence[str], _ods_ir.ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> LinkerOptionsOp:
  return LinkerOptionsOp(options=options, loc=loc, ip=ip)

