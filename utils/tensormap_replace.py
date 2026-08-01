
def tensormap_replace(field: _Union[_Any, _ods_ir.Attribute], addr: _ods_ir.Value, *, new_value: _Optional[_ods_ir.Value] = None, ord: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, new_value_attr: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TensormapReplaceOp:
  return TensormapReplaceOp(field=field, addr=addr, new_value=new_value, ord=ord, new_value_attr=new_value_attr, loc=loc, ip=ip)

