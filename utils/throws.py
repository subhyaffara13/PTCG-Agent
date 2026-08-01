
def throws(op, args, exc):
    try:
        op(*args)
    except type(exc):
        return sys.exc_info()[1].args == exc.args
    else:
        return False

