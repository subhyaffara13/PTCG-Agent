
def get_op_result_or_value(
    arg: _Union[
        _cext.ir.OpView, _cext.ir.Operation, _cext.ir.Value, _cext.ir.OpResultList
    ]
) -> _cext.ir.Value:
    """Returns the given value or the single result of the given op.

    This is useful to implement op constructors so that they can take other ops as
    arguments instead of requiring the caller to extract results for every op.
    Raises ValueError if provided with an op that doesn't have a single result.
    """
    if isinstance(arg, _cext.ir.OpView):
        return arg.operation.result
    elif isinstance(arg, _cext.ir.Operation):
        return arg.result
    elif isinstance(arg, _cext.ir.OpResultList):
        return arg[0]
    else:
        assert isinstance(arg, _cext.ir.Value), f"expects Value, got {type(arg)}"
        return arg

