
def extract_iteration_space(tensor: _ods_ir.Value[_ods_ir.RankedTensorType], lo_lvl: _Union[_Any, _ods_ir.IntegerAttr], hi_lvl: _Union[_Any, _ods_ir.IntegerAttr], *, parent_iter: _Optional[_ods_ir.Value] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExtractIterSpaceOp(tensor=tensor, loLvl=lo_lvl, hiLvl=hi_lvl, parentIter=parent_iter, results=results, loc=loc, ip=ip).result

