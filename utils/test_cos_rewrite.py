
def test_cos_rewrite():
    assert cos(x).rewrite(exp) == exp(I*x)/2 + exp(-I*x)/2
    assert cos(x).rewrite(tan) == (1 - tan(x/2)**2)/(1 + tan(x/2)**2)
    assert cos(x).rewrite(cot) == \
        Piecewise((1, Eq(im(x), 0) & Eq(Mod(x, 2*pi), 0)),
                  ((cot(x/2)**2 - 1)/(cot(x/2)**2 + 1), True))
    assert cos(sinh(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, sinh(3)).n()
    assert cos(cosh(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, cosh(3)).n()
    assert cos(tanh(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, tanh(3)).n()
    assert cos(coth(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, coth(3)).n()
    assert cos(sin(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, sin(3)).n()
    assert cos(cos(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, cos(3)).n()
    assert cos(tan(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, tan(3)).n()
    assert cos(cot(x)).rewrite(
        exp).subs(x, 3).n() == cos(x).rewrite(exp).subs(x, cot(3)).n()
    assert cos(log(x)).rewrite(Pow) == x**I/2 + x**-I/2
    assert cos(x).rewrite(sec) == 1/sec(x)
    assert cos(x).rewrite(sin) == sin(x + pi/2, evaluate=False)
    assert cos(x).rewrite(csc) == 1/csc(-x + pi/2, evaluate=False)
    assert cos(sin(x)).rewrite(Pow) == cos(sin(x))
    assert cos(x).rewrite(besselj) == Piecewise(
                (sqrt(pi*x/2)*besselj(-S.Half, x), Ne(x, 0)),
                (1, True)
            )
    assert cos(x).rewrite(besselj).subs(x, 0) == cos(0)

