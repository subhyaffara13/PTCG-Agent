
def test_hyperexpand_bases():
    assert hyperexpand(hyper([2], [a], z)) == \
        a + z**(-a + 1)*(-a**2 + 3*a + z*(a - 1) - 2)*exp(z)* \
        lowergamma(a - 1, z) - 1
    # TODO [a+1, aRational(-1, 2)], [2*a]
    assert hyperexpand(hyper([1, 2], [3], z)) == -2/z - 2*log(-z + 1)/z**2
    assert hyperexpand(hyper([S.Half, 2], [Rational(3, 2)], z)) == \
        -1/(2*z - 2) + atanh(sqrt(z))/sqrt(z)/2
    assert hyperexpand(hyper([S.Half, S.Half], [Rational(5, 2)], z)) == \
        (-3*z + 3)/4/(z*sqrt(-z + 1)) \
        + (6*z - 3)*asin(sqrt(z))/(4*z**Rational(3, 2))
    assert hyperexpand(hyper([1, 2], [Rational(3, 2)], z)) == -1/(2*z - 2) \
        - asin(sqrt(z))/(sqrt(z)*(2*z - 2)*sqrt(-z + 1))
    assert hyperexpand(hyper([Rational(-1, 2) - 1, 1, 2], [S.Half, 3], z)) == \
        sqrt(z)*(z*Rational(6, 7) - Rational(6, 5))*atanh(sqrt(z)) \
        + (-30*z**2 + 32*z - 6)/35/z - 6*log(-z + 1)/(35*z**2)
    assert hyperexpand(hyper([1 + S.Half, 1, 1], [2, 2], z)) == \
        -4*log(sqrt(-z + 1)/2 + S.Half)/z
    # TODO hyperexpand(hyper([a], [2*a + 1], z))
    # TODO [S.Half, a], [Rational(3, 2), a+1]
    assert hyperexpand(hyper([2], [b, 1], z)) == \
        z**(-b/2 + S.Half)*besseli(b - 1, 2*sqrt(z))*gamma(b) \
        + z**(-b/2 + 1)*besseli(b, 2*sqrt(z))*gamma(b)

