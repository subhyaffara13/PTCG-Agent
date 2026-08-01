
def device_async_wait(async_dependencies: _ods_ir.Value, *, num_groups: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DeviceAsyncWaitOp:
  return DeviceAsyncWaitOp(asyncDependencies=async_dependencies, numGroups=num_groups, loc=loc, ip=ip)

