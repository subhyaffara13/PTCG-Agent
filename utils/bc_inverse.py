
def bc_inverse(expr):
    if isinstance(expr.arg, BlockDiagMatrix):
        return expr.inverse()

    expr2 = blockinverse_1x1(expr)
    if expr != expr2:
        return expr2
    return blockinverse_2x2(Inverse(reblock_2x2(expr.arg)))

