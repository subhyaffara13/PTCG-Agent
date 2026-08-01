
def fence_proxy_acquire(scope: _Union[_Any, _ods_ir.Attribute], addr: _ods_ir.Value, size: _ods_ir.Value[_ods_ir.IntegerType], *, from_proxy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, to_proxy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> FenceProxyAcquireOp:
  return FenceProxyAcquireOp(scope=scope, addr=addr, size=size, fromProxy=from_proxy, toProxy=to_proxy, loc=loc, ip=ip)

