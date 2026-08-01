
def test_cot_rewrite():
    neg_exp, pos_exp = exp(-x*I), exp(x*I)
    assert cot(x).rewrite(exp) == I*(pos_exp + neg_exp)/(pos_exp - neg_exp)
    assert cot(x).rewrite(sin) == sin(2*x)/(2*(sin(x)**2))
    assert cot(x).rewrite(cos) == cos(x)/cos(x - pi/2, evaluate=False)
    assert cot(x).rewrite(tan) == 1/tan(x)
    def check(func):
        z = cot(func(x)).rewrite(exp) - cot(x).rewrite(exp).subs(x, func(x))
        assert z.rewrite(exp).expand() == 0
    check(sinh)
    check(cosh)
    check(tanh)
    check(coth)
    check(sin)
    check(cos)
    check(tan)
    assert cot(log(x)).rewrite(Pow) == -I*(x**-I + x**I)/(x**-I - x**I)
    assert cot(x).rewrite(sec) == sec(x - pi / 2, evaluate=False) / sec(x)
    assert cot(x).rewrite(csc) == csc(x) / csc(- x + pi / 2, evaluate=False)
    assert cot(sin(x)).rewrite(Pow) == cot(sin(x))
    assert cot(pi*Rational(2, 5), evaluate=False).rewrite(sqrt) == (Rational(-1, 4) + sqrt(5)/4)/\
                                                        sqrt(sqrt(5)/8 + Rational(5, 8))
    assert cot(x).rewrite(besselj) == besselj(-S.Half, x)/besselj(S.Half, x)
    assert cot(x).rewrite(besselj).subs(x, 0) == cot(0)

