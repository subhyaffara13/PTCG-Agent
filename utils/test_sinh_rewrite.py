
def test_sinh_rewrite():
    x = Symbol('x')
    assert sinh(x).rewrite(exp) == (exp(x) - exp(-x))/2 \
        == sinh(x).rewrite('tractable')
    assert sinh(x).rewrite(cosh) == -I*cosh(x + I*pi/2)
    tanh_half = tanh(S.Half*x)
    assert sinh(x).rewrite(tanh) == 2*tanh_half/(1 - tanh_half**2)
    coth_half = coth(S.Half*x)
    assert sinh(x).rewrite(coth) == 2*coth_half/(coth_half**2 - 1)

