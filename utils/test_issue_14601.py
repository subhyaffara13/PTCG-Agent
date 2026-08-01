
def test_issue_14601():
    e = 5*x*y/2 - y*(35*(x**3)/2 - 15*x/2)
    subst = {x:0.0, y:0.0}
    e2 = e.evalf(subs=subst)
    assert float(e2) == 0.0
    assert float((x + x*(x**2 + x)).evalf(subs={x: 0.0})) == 0.0

