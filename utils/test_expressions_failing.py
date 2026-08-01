
def test_expressions_failing():
    n = Symbol('n', integer=True, positive=True)
    assert residue(exp(z)/(z - pi*I/4*a)**n, z, I*pi*a) == \
        exp(I*pi*a/4)/factorial(n - 1)

