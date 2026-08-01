
def _function_to_dense(func, *args, **kwargs):
    return _MaskedToDense.apply(args[0])

