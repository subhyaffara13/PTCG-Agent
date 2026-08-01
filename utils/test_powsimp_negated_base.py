
def test_powsimp_negated_base():
    assert powsimp((-x + y)/sqrt(x - y)) == -sqrt(x - y)
    assert powsimp((-x + y)*(-z + y)/sqrt(x - y)/sqrt(z - y)) == sqrt(x - y)*sqrt(z - y)
    p = symbols('p', positive=True)
    reps = {p: 2, a: S.Half}
    assert powsimp((-p)**a/p**a).subs(reps) == ((-1)**a).subs(reps)
    assert powsimp((-p)**a*p**a).subs(reps) == ((-p**2)**a).subs(reps)
    n = symbols('n', negative=True)
    reps = {p: -2, a: S.Half}
    assert powsimp((-n)**a/n**a).subs(reps) == (-1)**(-a).subs(a, S.Half)
    assert powsimp((-n)**a*n**a).subs(reps) == ((-n**2)**a).subs(reps)
    # if x is 0 then the lhs is 0**a*oo**a which is not (-1)**a
    eq = (-x)**a/x**a
    assert powsimp(eq) == eq

