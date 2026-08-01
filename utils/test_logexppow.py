
def test_logexppow():   # no eval()
    x = Symbol('x', real=True)
    w = Symbol('w')
    e = (3**(1 + x) + 2**(1 + x))/(3**x + 2**x)
    assert e.subs(2**x, w) != e
    assert e.subs(exp(x*log(Rational(2))), w) != e

