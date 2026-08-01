
def test_heurisch_radicals():
    assert heurisch(1/sqrt(x), x) == 2*sqrt(x)
    assert heurisch(1/sqrt(x)**3, x) == -2/sqrt(x)
    assert heurisch(sqrt(x)**3, x) == 2*sqrt(x)**5/5

    assert heurisch(sin(x)*sqrt(cos(x)), x) == -2*sqrt(cos(x))**3/3
    y = Symbol('y')
    assert heurisch(sin(y*sqrt(x)), x) == 2/y**2*sin(y*sqrt(x)) - \
        2*sqrt(x)*cos(y*sqrt(x))/y
    assert heurisch_wrapper(sin(y*sqrt(x)), x) == Piecewise(
        (-2*sqrt(x)*cos(sqrt(x)*y)/y + 2*sin(sqrt(x)*y)/y**2, Ne(y, 0)),
        (0, True))
    y = Symbol('y', positive=True)
    assert heurisch_wrapper(sin(y*sqrt(x)), x) == 2/y**2*sin(y*sqrt(x)) - \
        2*sqrt(x)*cos(y*sqrt(x))/y

