
def _create_constants(*args, dtype):
    return tuple(ops.constant(a, dtype) for a in args)

