
def test_issue_15282():
    assert limit((x**2000 - (x + 1)**2000) / x**1999, x, oo) == -2000

