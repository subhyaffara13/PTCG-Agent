
def convert_floor(floor):
    val = convert_expr(floor.val)
    return sympy.floor(val, evaluate=False)

