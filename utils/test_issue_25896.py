
def test_issue_25896():
    # for both tests, C = 0 in log_to_real
    # but this only has a log result
    e = (2*x + 1)/(x**2 + x + 1) + 1/x
    assert ratint(e, x) == log(x**3 + x**2 + x)
    # while this has more
    assert ratint((4*x + 7)/(x**2 + 4*x + 6) + 2/x, x) == (
        2*log(x) + 2*log(x**2 + 4*x + 6) - sqrt(2)*atan(
        sqrt(2)*x/2 + sqrt(2))/2)

