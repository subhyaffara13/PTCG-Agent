
def test_sec_rewrite():
    assert sec(x).rewrite(exp) == 1/(exp(I*x)/2 + exp(-I*x)/2)
    assert sec(x).rewrite(cos) == 1/cos(x)
    assert sec(x).rewrite(tan) == (tan(x/2)**2 + 1)/(-tan(x/2)**2 + 1)
    assert sec(x).rewrite(pow) == sec(x)
    assert sec(x).rewrite(sqrt) == sec(x)
    assert sec(z).rewrite(cot) == (cot(z/2)**2 + 1)/(cot(z/2)**2 - 1)
    assert sec(x).rewrite(sin) == 1 / sin(x + pi / 2, evaluate=False)
    assert sec(x).rewrite(tan) == (tan(x / 2)**2 + 1) / (-tan(x / 2)**2 + 1)
    assert sec(x).rewrite(csc) == csc(-x + pi/2, evaluate=False)
    assert sec(x).rewrite(besselj) == Piecewise(
                (sqrt(2)/(sqrt(pi*x)*besselj(-S.Half, x)), Ne(x, 0)),
                (1, True)
            )
    assert sec(x).rewrite(besselj).subs(x, 0) == sec(0)

