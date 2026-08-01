
def make_global(*args):
    for arg in args:
        setattr(sys.modules[arg.__module__], arg.__name__, arg)

