
def st_bulk(addr: _ods_ir.Value, size: _ods_ir.Value[_ods_ir.IntegerType], *, init_val: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BulkStoreOp:
  return BulkStoreOp(addr=addr, size=size, initVal=init_val, loc=loc, ip=ip)

