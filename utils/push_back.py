
def push_back(cur_size: _ods_ir.Value[_ods_ir.IndexType], in_buffer: _ods_ir.Value[_ods_ir.MemRefType], value: _ods_ir.Value, *, n: _Optional[_ods_ir.Value[_ods_ir.IndexType]] = None, inbounds: _Optional[bool] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return PushBackOp(curSize=cur_size, inBuffer=in_buffer, value=value, n=n, inbounds=inbounds, results=results, loc=loc, ip=ip).results

