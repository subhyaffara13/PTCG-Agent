
def wmma_store(ptr: _ods_ir.Value, m: _Union[int, _ods_ir.IntegerAttr], n: _Union[int, _ods_ir.IntegerAttr], k: _Union[int, _ods_ir.IntegerAttr], layout: _Union[_Any, _ods_ir.Attribute], eltype: _Union[_Any, _ods_ir.Attribute], args: _Sequence[_ods_ir.Value], stride: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> WMMAStoreOp:
  return WMMAStoreOp(ptr=ptr, m=m, n=n, k=k, layout=layout, eltype=eltype, args=args, stride=stride, loc=loc, ip=ip)

