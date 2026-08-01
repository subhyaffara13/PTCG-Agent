
def test_factorial_moment():
    X = Poisson('X', 2)
    Y = Binomial('Y', 2, S.Half)
    Z = Hypergeometric('Z', 4, 2, 2)
    assert factorial_moment(X, 2) == 4
    assert factorial_moment(Y, 2) == S.Half
    assert factorial_moment(Z, 2) == Rational(1, 3)

    x, y, z, l = symbols('x y z l')
    Y = Binomial('Y', 2, y)
    Z = Hypergeometric('Z', 10, 2, 3)
    assert factorial_moment(Y, l) == y**2*FallingFactorial(
        2, l) + 2*y*(1 - y)*FallingFactorial(1, l) + (1 - y)**2*\
            FallingFactorial(0, l)
    assert factorial_moment(Z, l) == 7*FallingFactorial(0, l)/\
        15 + 7*FallingFactorial(1, l)/15 + FallingFactorial(2, l)/15

