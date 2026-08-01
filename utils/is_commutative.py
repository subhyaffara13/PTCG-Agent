
def is_commutative(x):
    if not isinstance(x, Compound):
        return False
    if sympy_commutative(x.op):
        return True
    if issubclass(x.op, Mul):
        return all(construct(arg).is_commutative for arg in x.args)


def is_commutative(x):
    return isinstance(x, Compound) and (x.op in ('CAdd', 'CMul'))

