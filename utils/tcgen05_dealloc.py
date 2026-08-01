
def tcgen05_dealloc(taddr: _ods_ir.Value, n_cols: _ods_ir.Value[_ods_ir.IntegerType], *, group: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Tcgen05DeallocOp:
  return Tcgen05DeallocOp(taddr=taddr, nCols=n_cols, group=group, loc=loc, ip=ip)

