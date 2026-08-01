
def test_issue_26250():
    e = elliptic_e(4*x/(x**2 + 2*x + 1))
    k = elliptic_k(4*x/(x**2 + 2*x + 1))
    e1 = ((1-3*x**2)*e**2/2 - (x**2-2*x+1)*e*k/2)
    e2 = pi**2*(x**8 - 2*x**7 - x**6 + 4*x**5 - x**4 - 2*x**3 + x**2)
    assert limit(e1/e2, x, 0) == -S(1)/8

