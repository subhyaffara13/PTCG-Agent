
def wmma_load(res: _ods_ir.Type, ptr: _ods_ir.Value, stride: _ods_ir.Value[_ods_ir.IntegerType], m: _Union[int, _ods_ir.IntegerAttr], n: _Union[int, _ods_ir.IntegerAttr], k: _Union[int, _ods_ir.IntegerAttr], layout: _Union[_Any, _ods_ir.Attribute], eltype: _Union[_Any, _ods_ir.Attribute], frag: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return WMMALoadOp(res=res, ptr=ptr, stride=stride, m=m, n=n, k=k, layout=layout, eltype=eltype, frag=frag, loc=loc, ip=ip).result

