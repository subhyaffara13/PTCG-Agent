
def test_commutative_in_commutative():
    from sympy.abc import a,b,c,d
    from sympy.functions.elementary.trigonometric import (cos, sin)
    eq = sin(3)*sin(4)*sin(5) + 4*cos(3)*cos(4)
    pat = a*cos(b)*cos(c) + d*sin(b)*sin(c)
    assert next(unify(eq, pat, variables=(a,b,c,d)))

