
def test_branch_bug():
    assert hyperexpand(hyper((Rational(-1, 3), S.Half), (Rational(2, 3), Rational(3, 2)), -z)) == \
        -z**S('1/3')*lowergamma(exp_polar(I*pi)/3, z)/5 \
        + sqrt(pi)*erf(sqrt(z))/(5*sqrt(z))
    assert hyperexpand(meijerg([Rational(7, 6), 1], [], [Rational(2, 3)], [Rational(1, 6), 0], z)) == \
        2*z**S('2/3')*(2*sqrt(pi)*erf(sqrt(z))/sqrt(z) - 2*lowergamma(
                       Rational(2, 3), z)/z**S('2/3'))*gamma(Rational(2, 3))/gamma(Rational(5, 3))


def test_branch_bug():
    from sympy.functions.special.gamma_functions import lowergamma
    from sympy.simplify.powsimp import powdenest
    # TODO gammasimp cannot prove that the factor is unity
    assert powdenest(integrate(erf(x**3), x, meijerg=True).diff(x),
           polar=True) == 2*erf(x**3)*gamma(Rational(2, 3))/3/gamma(Rational(5, 3))
    assert integrate(erf(x**3), x, meijerg=True) == \
        2*x*erf(x**3)*gamma(Rational(2, 3))/(3*gamma(Rational(5, 3))) \
        - 2*gamma(Rational(2, 3))*lowergamma(Rational(2, 3), x**6)/(3*sqrt(pi)*gamma(Rational(5, 3)))

