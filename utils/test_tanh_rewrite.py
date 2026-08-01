
def test_tanh_rewrite():
    x = Symbol('x')
    assert tanh(x).rewrite(exp) == (exp(x) - exp(-x))/(exp(x) + exp(-x)) \
        == tanh(x).rewrite('tractable')
    assert tanh(x).rewrite(sinh) == I*sinh(x)/sinh(I*pi/2 - x, evaluate=False)
    assert tanh(x).rewrite(cosh) == I*cosh(I*pi/2 - x, evaluate=False)/cosh(x)
    assert tanh(x).rewrite(coth) == 1/coth(x)

