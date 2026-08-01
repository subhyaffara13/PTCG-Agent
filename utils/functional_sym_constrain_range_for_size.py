
def functional_sym_constrain_range_for_size(size, min, max, dep_token):
    aten.sym_constrain_range_for_size(size, min=min, max=max)
    return dep_token

