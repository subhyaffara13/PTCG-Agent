
def test_issue_9326():
    from sympy.core.symbol import Dummy
    d1 = Dummy('d')
    d2 = Dummy('d')
    e = d1 + d2
    assert e.evalf(subs = {d1: 1, d2: 2}) == 3.0

