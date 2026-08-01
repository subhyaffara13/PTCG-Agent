
def source(func):
    s = f"File: {inspect.getsourcefile(func)}\n\n"
    s = s + inspect.getsource(func)
    return s


def source(func):
    s = 'File: %s\n\n' % inspect.getsourcefile(func)
    s = s + inspect.getsource(func)
    return s

