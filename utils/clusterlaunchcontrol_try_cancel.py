
def clusterlaunchcontrol_try_cancel(smem_address: _ods_ir.Value, mbarrier: _ods_ir.Value, *, multicast: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ClusterLaunchControlTryCancelOp:
  return ClusterLaunchControlTryCancelOp(smemAddress=smem_address, mbarrier=mbarrier, multicast=multicast, loc=loc, ip=ip)

