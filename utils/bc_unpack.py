
def bc_unpack(expr):
    if expr.blockshape == (1, 1):
        return expr.blocks[0, 0]
    return expr

