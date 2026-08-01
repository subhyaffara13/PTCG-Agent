
def test_issue_9855():
    #https://github.com/sympy/sympy/issues/9855
    x, y, z = symbols('x, y, z', real=True)
    s1 = Interval(1, x) & Interval(y, 2)
    s2 = Interval(1, 2)
    assert s1.is_subset(s2) == None

