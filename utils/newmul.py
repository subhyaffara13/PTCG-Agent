
def newmul(*args):
    if args[0] == 1:
        args = args[1:]
    return new(MatMul, *args)

