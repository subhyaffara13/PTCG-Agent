
def _find_arg(argname, args):
    for i, arg in enumerate(args):
        if arg.name == argname:
            return i, arg
    return None, None

