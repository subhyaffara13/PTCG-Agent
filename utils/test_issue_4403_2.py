
def test_issue_4403_2():
    assert integrate(sqrt(-x**2 - 4), x) == \
        -2*atan(x/sqrt(-4 - x**2)) + x*sqrt(-4 - x**2)/2

