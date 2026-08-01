
def reduce_local_int(val, func):
    return func(val.node._local_ints)

