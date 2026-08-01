
def fence_proxy_sync_restrict(order: _Union[_Any, _ods_ir.Attribute], *, from_proxy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, to_proxy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> FenceProxySyncRestrictOp:
  return FenceProxySyncRestrictOp(order=order, fromProxy=from_proxy, toProxy=to_proxy, loc=loc, ip=ip)

