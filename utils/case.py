
def case(request):
    """
    Fixture for all cases in IterativeParams
    """
    return request.param


def case(result: _Sequence[_ods_ir.Type], index: _ods_ir.Value, num_branches: int, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CaseOp]:
  op = CaseOp(result=result, index=index, num_branches=num_branches, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def case(result: _Sequence[_ods_ir.Type], index: _ods_ir.Value[_ods_ir.RankedTensorType], num_branches: int, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CaseOp]:
  op = CaseOp(result=result, index=index, num_branches=num_branches, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

