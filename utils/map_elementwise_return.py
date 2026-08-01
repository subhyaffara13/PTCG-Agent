
def map_elementwise_return(result: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MapElementwiseReturnOp:
  return MapElementwiseReturnOp(result=result, loc=loc, ip=ip)

