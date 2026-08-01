
def unpack_variables(args):
    if isinstance(args, tuple):
        return tuple(unpack_variables(elem) for elem in args)
    else:
        return args

