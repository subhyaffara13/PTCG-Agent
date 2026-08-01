
def test_issue_9983():
    n = Symbol('n', integer=True, positive=True)
    p = Product(1 + 1/n**Rational(2, 3), (n, 1, oo))
    assert p.is_convergent() is S.false
    assert product(1 + 1/n**Rational(2, 3), (n, 1, oo)) == p.doit()

