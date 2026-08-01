
def int_func(request):
    return (request.param, INT_FUNCS[request.param],
            INT_FUNC_HASHES[request.param])

