
def _printable(arg):
    return String(arg) if isinstance(arg, str) else sympify(arg)

