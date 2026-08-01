
def coiterate(results_: _Sequence[_ods_ir.Type], iter_spaces: _Sequence[_ods_ir.Value], init_args: _Sequence[_ods_ir.Value], crd_used_lvls: _Union[_Any, _ods_ir.IntegerAttr], cases: _Union[_Any, _ods_ir.ArrayAttr], num_case_regions: int, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CoIterateOp]:
  op = CoIterateOp(results_=results_, iterSpaces=iter_spaces, initArgs=init_args, crdUsedLvls=crd_used_lvls, cases=cases, num_caseRegions=num_case_regions, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

