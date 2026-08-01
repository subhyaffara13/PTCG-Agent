
def clusterlaunchcontrol_query_cancel(query_type: _Union[_Any, _ods_ir.Attribute], try_cancel_response: _ods_ir.Value[_ods_ir.IntegerType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ClusterLaunchControlQueryCancelOp(query_type=query_type, try_cancel_response=try_cancel_response, results=results, loc=loc, ip=ip).result

