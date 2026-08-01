
def test_pr_23583():
    # This result from meijerg is wrong. Check whether new result is correct when this test fail.
    assert integrate(1/sqrt((x - I)**2-1)) == Piecewise((acosh(x - I), Abs((x - I)**2) > 1), (-I*asin(x - I), True))


def test_pr_23583():
    # This result is wrong. Check whether new result is correct when this test fail.
    assert integrate(1/sqrt((x - I)**2-1), meijerg=True) == \
           Piecewise((acosh(x - I), Abs((x - I)**2) > 1), (-I*asin(x - I), True))

