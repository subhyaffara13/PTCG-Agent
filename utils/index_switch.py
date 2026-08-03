from typing import Union

def index_switch(
    results,
    arg,
    cases,
    case_body_builder=None,
    default_body_builder=None,
    loc=None,
    ip=None,
) -> Union[OpResult, OpResultList, IndexSwitchOp]:
    op = IndexSwitchOp(
        results=results,
        arg=arg,
        cases=cases,
        case_body_builder=case_body_builder,
        default_body_builder=default_body_builder,
        loc=loc,
        ip=ip,
    )
    return _get_op_result_or_op_results(op)


def index_switch(results_: _Sequence[_ods_ir.Type], arg: _ods_ir.Value[_ods_ir.IndexType], cases: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], num_case_regions: int, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, IndexSwitchOp]:
  op = IndexSwitchOp(results_=results_, arg=arg, cases=cases, num_caseRegions=num_case_regions, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

