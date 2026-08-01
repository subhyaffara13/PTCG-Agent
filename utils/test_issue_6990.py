
def test_issue_6990():
    assert (sqrt(a + b*x + x**2)).series(x, 0, 3).removeO() == \
        sqrt(a)*x**2*(1/(2*a) - b**2/(8*a**2)) + sqrt(a) + b*x/(2*sqrt(a))

