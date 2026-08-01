
def tcgen05_ld_red(data: _ods_ir.Type, red_val: _ods_ir.Type, shape: _Union[_Any, _ods_ir.Attribute], op: _Union[_Any, _ods_ir.Attribute], addr: _ods_ir.Value, *, abs: _Optional[bool] = None, nan: _Optional[bool] = None, offset: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return Tcgen05LdRedOp(data=data, redVal=red_val, shape=shape, op=op, addr=addr, abs=abs, nan=nan, offset=offset, loc=loc, ip=ip).results

