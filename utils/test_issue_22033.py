
def test_issue_22033():
    xr = Symbol('xr', real=True)
    e = (1/xr)
    assert e.subs(xr**2, y) == e

