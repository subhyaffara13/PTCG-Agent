
def test_issue_10503():
    f = exp(x**3)*cos(x**6)
    assert f.series(x, 0, 14) == 1 + x**3 + x**6/2 + x**9/6 - 11*x**12/24 + O(x**14)

