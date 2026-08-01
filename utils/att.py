
def att(*args):
    if len(args) == 4:
        return AntiSymmetricTensor('t', args[:2], args[2:] )
    elif len(args) == 2:
        return AntiSymmetricTensor('t', (args[0],), (args[1],))

