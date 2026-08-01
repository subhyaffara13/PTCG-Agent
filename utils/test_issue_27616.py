
def test_issue_27616():
    #https://github.com/sympy/sympy/issues/27616
    N = 9804659461513846513 + 1
    assert qs(N, 5000, 20000) is not None

