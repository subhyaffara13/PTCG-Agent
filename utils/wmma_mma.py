
def wmma_mma(res: _ods_ir.Type, m: _Union[int, _ods_ir.IntegerAttr], n: _Union[int, _ods_ir.IntegerAttr], k: _Union[int, _ods_ir.IntegerAttr], layout_a: _Union[_Any, _ods_ir.Attribute], layout_b: _Union[_Any, _ods_ir.Attribute], eltype_a: _Union[_Any, _ods_ir.Attribute], eltype_b: _Union[_Any, _ods_ir.Attribute], args: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return WMMAMmaOp(res=res, m=m, n=n, k=k, layoutA=layout_a, layoutB=layout_b, eltypeA=eltype_a, eltypeB=eltype_b, args=args, loc=loc, ip=ip).result

