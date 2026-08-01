
def convert_comp(comp):
    if comp.group():
        return convert_expr(comp.group().expr())
    elif comp.abs_group():
        return sympy.Abs(convert_expr(comp.abs_group().expr()), evaluate=False)
    elif comp.atom():
        return convert_atom(comp.atom())
    elif comp.floor():
        return convert_floor(comp.floor())
    elif comp.ceil():
        return convert_ceil(comp.ceil())
    elif comp.func():
        return convert_func(comp.func())

