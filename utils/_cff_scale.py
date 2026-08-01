
def _cff_scale(visitor, args):
    for i, arg in enumerate(args):
        if not isinstance(arg, list):
            if not isinstance(arg, bytes):
                args[i] = visitor.scale(arg)
        else:
            num_blends = arg[-1]
            _cff_scale(visitor, arg)
            arg[-1] = num_blends

