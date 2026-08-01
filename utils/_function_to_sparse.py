
def _function_to_sparse(func, *args, **kwargs):
    return _MaskedToSparse.apply(args[0])

