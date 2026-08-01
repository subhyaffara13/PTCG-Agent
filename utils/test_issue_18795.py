
def test_issue_18795():
    r = Symbol('r', real=True)
    a = B(-1,1)
    c = B(7, oo)
    b = B(-oo, oo)
    assert c - tan(r) == B(7-tan(r), oo)
    assert b + tan(r) == B(-oo, oo)
    assert (a + r)/a == B(-oo, oo)*B(r - 1, r + 1)
    assert (b + a)/a == B(-oo, oo)

