
def test_issue_6844():
    f = y(n + 2) - y(n + 1) + y(n)/4
    assert rsolve(f, y(n)) == 2**(-n + 1)*C1*n + 2**(-n)*C0
    assert rsolve(f, y(n), {y(0): 0, y(1): 1}) == 2**(1 - n)*n

