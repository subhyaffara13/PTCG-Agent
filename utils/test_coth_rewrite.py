
def test_coth_rewrite():
    x = Symbol('x')
    assert coth(x).rewrite(exp) == (exp(x) + exp(-x))/(exp(x) - exp(-x)) \
        == coth(x).rewrite('tractable')
    assert coth(x).rewrite(sinh) == -I*sinh(I*pi/2 - x, evaluate=False)/sinh(x)
    assert coth(x).rewrite(cosh) == -I*cosh(x)/cosh(I*pi/2 - x, evaluate=False)
    assert coth(x).rewrite(tanh) == 1/tanh(x)

