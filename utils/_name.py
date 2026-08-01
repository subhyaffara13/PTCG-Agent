
def _name(arg):
    if hasattr(arg, 'name'):
        return arg.name
    else:
        return String(arg)

