
def _flatten_args(args, _cls):
    temp_args = []
    for arg in args:
        if isinstance(arg, _cls):
            temp_args.extend(arg.args)
        else:
            temp_args.append(arg)
    return tuple(temp_args)

