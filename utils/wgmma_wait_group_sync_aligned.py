
def wgmma_wait_group_sync_aligned(group: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> WgmmaWaitGroupSyncOp:
  return WgmmaWaitGroupSyncOp(group=group, loc=loc, ip=ip)

