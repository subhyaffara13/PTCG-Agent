
def get_op_result_or_op_results(
    op: _Union[_cext.ir.OpView, _cext.ir.Operation],
) -> _Union[_cext.ir.Operation, _cext.ir.OpResult, _Sequence[_cext.ir.OpResult]]:
    results = op.results
    num_results = len(results)
    if num_results == 1:
        return results[0]
    elif num_results > 1:
        return results
    elif isinstance(op, _cext.ir.OpView):
        return op.operation
    else:
        return op

