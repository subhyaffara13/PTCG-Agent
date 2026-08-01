
def global_(sym_name: _Union[str, _ods_ir.StringAttr], type_: _Union[_Any, _ods_ir.TypeAttr], *, sym_visibility: _Optional[_Union[str, _ods_ir.StringAttr]] = None, initial_value: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, constant: _Optional[bool] = None, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> GlobalOp:
  return GlobalOp(sym_name=sym_name, type_=type_, sym_visibility=sym_visibility, initial_value=initial_value, constant=constant, alignment=alignment, loc=loc, ip=ip)

