
def test_hyperexpand_parametric():
    assert hyperexpand(hyper([a, S.Half + a], [S.Half], z)) \
        == (1 + sqrt(z))**(-2*a)/2 + (1 - sqrt(z))**(-2*a)/2
    assert hyperexpand(hyper([a, Rational(-1, 2) + a], [2*a], z)) \
        == 2**(2*a - 1)*((-z + 1)**S.Half + 1)**(-2*a + 1)

