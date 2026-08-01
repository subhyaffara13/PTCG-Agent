
def warp_execute_on_lane_0(results_: _Sequence[_ods_ir.Type], laneid: _ods_ir.Value[_ods_ir.IndexType], warp_size: _Union[int, _ods_ir.IntegerAttr], args: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, WarpExecuteOnLane0Op]:
  op = WarpExecuteOnLane0Op(results_=results_, laneid=laneid, warp_size=warp_size, args=args, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

