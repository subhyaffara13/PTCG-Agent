import functools

def _share_masks(*args, xp):
    if is_marray(xp):
        mask = functools.reduce(operator.or_, (arg.mask for arg in args))
        args = [xp.asarray(arg.data, mask=mask) for arg in args]
    return args[0] if len(args) == 1 else args

