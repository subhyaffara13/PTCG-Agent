
def tcgen05_commit(addr: _ods_ir.Value, *, multicast_mask: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, group: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Tcgen05CommitOp:
  return Tcgen05CommitOp(addr=addr, multicastMask=multicast_mask, group=group, loc=loc, ip=ip)

