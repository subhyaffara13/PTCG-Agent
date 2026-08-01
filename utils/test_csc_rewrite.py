
def test_csc_rewrite():
    assert csc(x).rewrite(pow) == csc(x)
    assert csc(x).rewrite(sqrt) == csc(x)

    assert csc(x).rewrite(exp) == 2*I/(exp(I*x) - exp(-I*x))
    assert csc(x).rewrite(sin) == 1/sin(x)
    assert csc(x).rewrite(tan) == (tan(x/2)**2 + 1)/(2*tan(x/2))
    assert csc(x).rewrite(cot) == (cot(x/2)**2 + 1)/(2*cot(x/2))
    assert csc(x).rewrite(cos) == 1/cos(x - pi/2, evaluate=False)
    assert csc(x).rewrite(sec) == sec(-x + pi/2, evaluate=False)

    # issue 17349
    assert csc(1 - exp(-besselj(I, I))).rewrite(cos) == \
           -1/cos(-pi/2 - 1 + cos(I*besselj(I, I)) +
                  I*cos(-pi/2 + I*besselj(I, I), evaluate=False), evaluate=False)
    assert csc(x).rewrite(besselj) == sqrt(2)/(sqrt(pi*x)*besselj(S.Half, x))
    assert csc(x).rewrite(besselj).subs(x, 0) == csc(0)

