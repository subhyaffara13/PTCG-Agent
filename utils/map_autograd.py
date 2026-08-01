
def map_autograd(f, xs, pos_args):
    num_mapped_args = len(xs)
    flat_out = MapAutogradOp.apply(f, num_mapped_args, *xs, *pos_args)
    return flat_out

