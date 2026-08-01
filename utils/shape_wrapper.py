
def shape_wrapper(f):
    @wraps(f)
    def nf(*args, out_val=None, **kwargs):
        args, kwargs, out_shape = tree_map(get_shape, (args, kwargs, out_val))
        return f(*args, out_shape=out_shape, **kwargs)
    return nf

