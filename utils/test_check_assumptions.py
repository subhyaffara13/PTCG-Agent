
def test_check_assumptions():
    x = symbols('x', positive=True)
    assert solve(x**2 - 1) == [1]


def test_check_assumptions():
    assert check_assumptions(1, 0) is False
    x = Symbol('x', positive=True)
    assert check_assumptions(1, x) is True
    assert check_assumptions(1, 1) is True
    assert check_assumptions(-1, 1) is False
    i = Symbol('i', integer=True)
    # don't know if i is positive (or prime, etc...)
    assert check_assumptions(i, 1) is None
    assert check_assumptions(Dummy(integer=None), integer=True) is None
    assert check_assumptions(Dummy(integer=None), integer=False) is None
    assert check_assumptions(Dummy(integer=False), integer=True) is False
    assert check_assumptions(Dummy(integer=True), integer=False) is False
    # no T/F assumptions to check
    assert check_assumptions(Dummy(integer=False), integer=None) is True
    raises(ValueError, lambda: check_assumptions(2*x, x, positive=True))

