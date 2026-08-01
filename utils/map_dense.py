
def map_dense(f, xs, pos_args):
    pytrees = [f(*inp, *pos_args) for inp in _unstack_pytree(xs)]
    return _stack_pytree(pytrees)

