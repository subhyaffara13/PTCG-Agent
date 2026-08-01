
def mlir_alias(alias_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], sym_name: _Union[str, _ods_ir.StringAttr], linkage: _Union[_Any, _ods_ir.Attribute], *, dso_local: _Optional[bool] = None, thread_local_: _Optional[bool] = None, unnamed_addr: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, visibility_: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> AliasOp:
  return AliasOp(alias_type=alias_type, sym_name=sym_name, linkage=linkage, dso_local=dso_local, thread_local_=thread_local_, unnamed_addr=unnamed_addr, visibility_=visibility_, loc=loc, ip=ip)

