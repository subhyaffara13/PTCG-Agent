
def tcgen05_st(shape: _Union[_Any, _ods_ir.Attribute], tmem_addr: _ods_ir.Value, val: _ods_ir.Value, *, unpack: _Optional[bool] = None, offset: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Tcgen05StOp:
  return Tcgen05StOp(shape=shape, tmemAddr=tmem_addr, val=val, unpack=unpack, offset=offset, loc=loc, ip=ip)

