
def is_associative(x):
    return isinstance(x, Compound) and sympy_associative(x.op)


def is_associative(x):
    return isinstance(x, Compound) and (x.op in ('Add', 'Mul', 'CAdd', 'CMul'))

