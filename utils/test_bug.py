
def test_bug():
    h = hyper([-1, 1], [z], -1)
    assert hyperexpand(h) == (z + 1)/z


def test_bug():
    assert residue(2**(z)*(s + z)*(1 - s - z)/z**2, z, 0) == \
        1 + s*log(2) - s**2*log(2) - 2*s


def test_bug():
    x1 = Symbol('x1')
    x2 = Symbol('x2')
    y = x1*x2
    assert y.subs(x1, Float(3.0)) == Float(3.0)*x2

