
def hadamard_power(base, exp):
    base = sympify(base)
    exp = sympify(exp)
    if exp == 1:
        return base
    if not base.is_Matrix:
        return base**exp
    if exp.is_Matrix:
        raise ValueError("cannot raise expression to a matrix")
    return HadamardPower(base, exp)

