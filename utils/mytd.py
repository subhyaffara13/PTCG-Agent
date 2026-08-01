
def mytd(expr1, expr2, x):
    from sympy.core.random import test_derivative_numerically, \
        random_complex_number
    subs = {}
    for a in expr1.free_symbols:
        if a != x:
            subs[a] = random_complex_number()
    return expr1.diff(x) == expr2 and test_derivative_numerically(expr1.subs(subs), x)

