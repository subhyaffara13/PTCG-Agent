
def test_issue_13416():
    assert limit((-x**3*log(x)**3 + (x - 1)*(x + 1)**2*log(x + 1)**3)/(x**2*log(x)**3), x, oo) == 1

