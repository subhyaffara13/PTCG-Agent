
def test_exp_assumptions():
    r = Symbol('r', real=True)
    i = Symbol('i', imaginary=True)
    for e in exp, exp_polar:
        assert e(x).is_real is None
        assert e(x).is_imaginary is None
        assert e(i).is_real is None
        assert e(i).is_imaginary is None
        assert e(r).is_real is True
        assert e(r).is_imaginary is False
        assert e(re(x)).is_extended_real is True
        assert e(re(x)).is_imaginary is False

    assert Pow(E, I*pi, evaluate=False).is_imaginary == False
    assert Pow(E, 2*I*pi, evaluate=False).is_imaginary == False
    assert Pow(E, I*pi/2, evaluate=False).is_imaginary == True
    assert Pow(E, I*pi/3, evaluate=False).is_imaginary is None

    assert exp(0, evaluate=False).is_algebraic

    a = Symbol('a', algebraic=True)
    an = Symbol('an', algebraic=True, nonzero=True)
    r = Symbol('r', rational=True)
    rn = Symbol('rn', rational=True, nonzero=True)
    assert exp(a).is_algebraic is None
    assert exp(an).is_algebraic is False
    assert exp(pi*r).is_algebraic is None
    assert exp(pi*rn).is_algebraic is False

    assert exp(0, evaluate=False).is_algebraic is True
    assert exp(I*pi/3, evaluate=False).is_algebraic is True
    assert exp(I*pi*r, evaluate=False).is_algebraic is True

