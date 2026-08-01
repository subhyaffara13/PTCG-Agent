
def ubound(array, dim=None, kind=None):
    return FunctionCall(
        'ubound',
        [_printable(array)] +
        ([_printable(dim)] if dim else []) +
        ([_printable(kind)] if kind else [])
    )

