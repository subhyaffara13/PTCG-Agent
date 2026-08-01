
def test_issue_13340():
    eq = Poly(y**3 + exp(x)*y + x, y, domain='EX')
    roots_d = roots(eq)
    assert len(roots_d) == 3

