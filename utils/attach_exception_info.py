
def attach_exception_info(e, name):
    if e.args and type(e.args[0]) is str:
        e.args = ('%s: %s' % (name, e.args[0]),) + e.args[1:]

