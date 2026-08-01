
def test_issue_25165():
    e1 = (1/sqrt(( - x + 1)**2 + (x - 0.23)**4)).series(x, 0, 2)
    e2 = 0.998603724830355 + 1.02004923189934*x + O(x**2)
    assert all_close(e1, e2)

