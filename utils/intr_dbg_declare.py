
def intr_dbg_declare(addr: _ods_ir.Value, var_info: _Union[_Any, _ods_ir.Attribute], *, location_expr: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DbgDeclareOp:
  return DbgDeclareOp(addr=addr, varInfo=var_info, locationExpr=location_expr, loc=loc, ip=ip)

