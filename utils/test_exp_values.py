
def test_exp_values():
    if global_parameters.exp_is_pow:
        assert type(exp(x)) is Pow
    else:
        assert type(exp(x)) is exp

    k = Symbol('k', integer=True)

    assert exp(nan) is nan

    assert exp(oo) is oo
    assert exp(-oo) == 0

    assert exp(0) == 1
    assert exp(1) == E
    assert exp(-1 + x).as_base_exp() == (S.Exp1, x - 1)
    assert exp(1 + x).as_base_exp() == (S.Exp1, x + 1)

    assert exp(pi*I/2) == I
    assert exp(pi*I) == -1
    assert exp(pi*I*Rational(3, 2)) == -I
    assert exp(2*pi*I) == 1

    assert refine(exp(pi*I*2*k)) == 1
    assert refine(exp(pi*I*2*(k + S.Half))) == -1
    assert refine(exp(pi*I*2*(k + Rational(1, 4)))) == I
    assert refine(exp(pi*I*2*(k + Rational(3, 4)))) == -I

    assert exp(log(x)) == x
    assert exp(2*log(x)) == x**2
    assert exp(pi*log(x)) == x**pi

    assert exp(17*log(x) + E*log(y)) == x**17 * y**E

    assert exp(x*log(x)) != x**x
    assert exp(sin(x)*log(x)) != x

    assert exp(3*log(x) + oo*x) == exp(oo*x) * x**3
    assert exp(4*log(x)*log(y) + 3*log(x)) == x**3 * exp(4*log(x)*log(y))

    assert exp(-oo, evaluate=False).is_finite is True
    assert exp(oo, evaluate=False).is_finite is False

