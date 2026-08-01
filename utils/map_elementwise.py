
def map_elementwise(result: _Sequence[_ods_ir.Type], srcs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], pack: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, MapElementwiseOp]:
  op = MapElementwiseOp(result=result, srcs=srcs, pack=pack, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

