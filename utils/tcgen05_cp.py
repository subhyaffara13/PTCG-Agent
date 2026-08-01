
def tcgen05_cp(shape: _Union[_Any, _ods_ir.Attribute], taddr: _ods_ir.Value, smem_desc: _ods_ir.Value[_ods_ir.IntegerType], *, group: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, multicast: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, src_format: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Tcgen05CpOp:
  return Tcgen05CpOp(shape=shape, taddr=taddr, smem_desc=smem_desc, group=group, multicast=multicast, srcFormat=src_format, loc=loc, ip=ip)

