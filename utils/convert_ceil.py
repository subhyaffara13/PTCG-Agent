
def convert_ceil(ceil):
    val = convert_expr(ceil.val)
    return sympy.ceiling(val, evaluate=False)

