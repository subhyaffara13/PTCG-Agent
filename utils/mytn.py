
def mytn(expr1, expr2, expr3, x, d=0):
    from sympy.core.random import verify_numerically, random_complex_number
    subs = {}
    for a in expr1.free_symbols:
        if a != x:
            subs[a] = random_complex_number()
    return expr2 == expr3 and verify_numerically(expr1.subs(subs),
                                               expr2.subs(subs), x, d=d)

