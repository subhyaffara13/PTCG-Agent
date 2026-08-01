
def test_issue_4825():
    raises(ValueError, lambda: dsolve(f(x, y).diff(x) - y*f(x, y), f(x)))
    assert classify_ode(f(x, y).diff(x) - y*f(x, y), f(x), dict=True) == \
        {'order': 0, 'default': None, 'ordered_hints': ()}
    # See also issue 3793, test Z13.
    raises(ValueError, lambda: dsolve(f(x).diff(x), f(y)))
    assert classify_ode(f(x).diff(x), f(y), dict=True) == \
        {'order': 0, 'default': None, 'ordered_hints': ()}

