
def test_substitute_dummies_new_indices():
    i, j = symbols('i j', below_fermi=True, cls=Dummy)
    a, b = symbols('a b', above_fermi=True, cls=Dummy)
    p, q = symbols('p q', cls=Dummy)
    f = Function('f')
    assert substitute_dummies(f(i, a, p) - f(j, b, q), new_indices=True) == 0

