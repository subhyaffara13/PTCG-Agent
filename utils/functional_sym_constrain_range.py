
def functional_sym_constrain_range(size, min=None, max=None, dep_token=None):
    aten.sym_constrain_range(size, min=min, max=max)
    return dep_token

