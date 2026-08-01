
def test_algebraic():
    assert ask(Q.algebraic(x)) is None

    assert ask(Q.algebraic(I)) is True
    assert ask(Q.algebraic(2*I)) is True
    assert ask(Q.algebraic(I/3)) is True

    assert ask(Q.algebraic(sqrt(7))) is True
    assert ask(Q.algebraic(2*sqrt(7))) is True
    assert ask(Q.algebraic(sqrt(7)/3)) is True

    assert ask(Q.algebraic(I*sqrt(3))) is True
    assert ask(Q.algebraic(sqrt(1 + I*sqrt(3)))) is True

    assert ask(Q.algebraic(1 + I*sqrt(3)**Rational(17, 31))) is True
    assert ask(Q.algebraic(1 + I*sqrt(3)**(17/pi))) is None

    for f in [exp, sin, tan, asin, atan, cos]:
        assert ask(Q.algebraic(f(7))) is False
        assert ask(Q.algebraic(f(7, evaluate=False))) is False
        assert ask(Q.algebraic(f(0, evaluate=False))) is True
        assert ask(Q.algebraic(f(x)), Q.algebraic(x)) is None
        assert ask(Q.algebraic(f(x)), Q.algebraic(x) & Q.nonzero(x)) is False

    for g in [log, acos]:
        assert ask(Q.algebraic(g(7))) is False
        assert ask(Q.algebraic(g(7, evaluate=False))) is False
        assert ask(Q.algebraic(g(1, evaluate=False))) is True
        assert ask(Q.algebraic(g(x)), Q.algebraic(x)) is None
        assert ask(Q.algebraic(g(x)), Q.algebraic(x) & Q.nonzero(x - 1)) is False

    for h in [cot, acot]:
        assert ask(Q.algebraic(h(7))) is False
        assert ask(Q.algebraic(h(7, evaluate=False))) is False
        assert ask(Q.algebraic(h(x)), Q.algebraic(x)) is False

    assert ask(Q.algebraic(sqrt(sin(7)))) is None
    assert ask(Q.algebraic(sqrt(y + I*sqrt(7)))) is None

    assert ask(Q.algebraic(2.47)) is True

    assert ask(Q.algebraic(x), Q.transcendental(x)) is False
    assert ask(Q.transcendental(x), Q.algebraic(x)) is False

    #https://github.com/sympy/sympy/issues/27445
    assert ask(Q.algebraic(Pow(1, x, evaluate=False)), Q.algebraic(x)) is None
    assert ask(Q.algebraic(Pow(x, y))) is None
    assert ask(Q.algebraic(Pow(1, x, evaluate=False))) is None
    assert ask(Q.algebraic(x**(pi*I))) is None
    assert ask(Q.algebraic(pi**n),Q.integer(n) & Q.positive(n)) is False
    assert ask(Q.algebraic(x**y),Q.algebraic(x) & Q.rational(y)) is True

