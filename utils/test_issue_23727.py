
def test_issue_23727():
    res = series(sqrt(1 - x**2), x, 0.1)
    assert res.is_Add == True

