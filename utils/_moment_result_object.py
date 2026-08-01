
def _moment_result_object(*args):
    if len(args) == 1:
        return args[0]
    xp = array_namespace(*args)
    return xp.stack(args)

