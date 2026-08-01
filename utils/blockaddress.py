
def blockaddress(res: _ods_ir.Type, block_addr: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BlockAddressOp(res=res, block_addr=block_addr, loc=loc, ip=ip).result

