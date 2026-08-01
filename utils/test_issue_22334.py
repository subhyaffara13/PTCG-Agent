
def test_issue_22334():
    k, n  = symbols('k, n', positive=True)
    assert limit((n+1)**k/((n+1)**(k+1) - (n)**(k+1)), n, oo) == 1/(k + 1)
    assert limit((n+1)**k/((n+1)**(k+1) - (n)**(k+1)).expand(), n, oo) == 1/(k + 1)
    assert limit((n+1)**k/(n*(-n**k + (n + 1)**k) + (n + 1)**k), n, oo) == 1/(k + 1)

