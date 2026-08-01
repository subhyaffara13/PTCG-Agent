
def _torch_reduce(fn):
    def reduce_fn(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            return _torch_reduce_all(fn)(args[0])
        return _torch_reduce_dim(fn)(*args, **kwargs)

    return reduce_fn

