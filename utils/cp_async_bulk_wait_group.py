
def cp_async_bulk_wait_group(group: _Union[int, _ods_ir.IntegerAttr], *, read: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncBulkWaitGroupOp:
  return CpAsyncBulkWaitGroupOp(group=group, read=read, loc=loc, ip=ip)

