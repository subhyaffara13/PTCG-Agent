
def test_rewrite1():
    e = exp(x)
    assert mrewrite(mrv(e, x), x, m) == (1/m, -x)
    e = exp(x**2)
    assert mrewrite(mrv(e, x), x, m) == (1/m, -x**2)
    e = exp(x + 1/x)
    assert mrewrite(mrv(e, x), x, m) == (1/m, -x - 1/x)
    e = 1/exp(-x + exp(-x)) - exp(x)
    assert mrewrite(mrv(e, x), x, m) == ((-m*exp(m) + m)*exp(-m)/m**2, -x)


def test_rewrite1():
    assert _rewrite1(x**3*meijerg([a], [b], [c], [d], x**2 + y*x**2)*5, x) == \
        (5, x**3, [(1, 0, meijerg([a], [b], [c], [d], x**2*(y + 1)))], True)

