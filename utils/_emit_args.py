
def _emit_args(indent, arguments):
    return ",".join(_emit_arg(indent, i, arg) for i, arg in enumerate(arguments))

