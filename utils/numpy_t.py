
def numpy_T(g: jit_utils.GraphContext, input):
    ndim = symbolic_helper._get_tensor_rank(input)
    if ndim is None:
        raise AssertionError("ndim must be non-None")
    perm = list(reversed(range(ndim)))
    return g.op("Transpose", input, perm_i=perm)

