
def test_issue_6419_6421():
    assert (1/(1 + x/y)).subs(x/y, x) == 1/(1 + x)
    assert (-2*I).subs(2*I, x) == -x
    assert (-I*x).subs(I*x, x) == -x
    assert (-3*I*y**4).subs(3*I*y**2, x) == -x*y**2

