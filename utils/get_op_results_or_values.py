
def get_op_results_or_values(
    arg: _Union[
        _cext.ir.OpView,
        _cext.ir.Operation,
        _Sequence[_Union[_cext.ir.OpView, _cext.ir.Operation, _cext.ir.Value]],
    ]
) -> _Union[
    _Sequence[_Union[_cext.ir.OpView, _cext.ir.Operation, _cext.ir.Value]],
    _cext.ir.OpResultList,
]:
    """Returns the given sequence of values or the results of the given op.

    This is useful to implement op constructors so that they can take other ops as
    lists of arguments instead of requiring the caller to extract results for
    every op.
    """
    if isinstance(arg, _cext.ir.OpView):
        return arg.operation.results
    elif isinstance(arg, _cext.ir.Operation):
        return arg.results
    else:
        return arg

