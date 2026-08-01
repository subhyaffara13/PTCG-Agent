
def test_heurisch_wrapper():
    f = 1/(y + x)
    assert heurisch_wrapper(f, x) == log(x + y)
    f = 1/(y - x)
    assert heurisch_wrapper(f, x) == -log(x - y)
    f = 1/((y - x)*(y + x))
    assert heurisch_wrapper(f, x) == Piecewise(
        (-log(x - y)/(2*y) + log(x + y)/(2*y), Ne(y, 0)), (1/x, True))
    # issue 6926
    f = sqrt(x**2/((y - x)*(y + x)))
    assert heurisch_wrapper(f, x) == x*sqrt(-x**2/(x**2 - y**2)) \
    - y**2*sqrt(-x**2/(x**2 - y**2))/x

