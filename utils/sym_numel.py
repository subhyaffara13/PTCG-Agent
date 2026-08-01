
def sym_numel(t):
    return functools.reduce(operator.mul, t.shape, 1)


def sym_numel(a):
    return a.get_numel()

