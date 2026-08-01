
def test_substitute_dummies_substitution_order():
    i, j, k, l = symbols('i j k l', below_fermi=True, cls=Dummy)
    f = Function('f')
    from sympy.utilities.iterables import variations
    for permut in variations([i, j, k, l], 4):
        assert substitute_dummies(f(*permut) - f(i, j, k, l)) == 0

