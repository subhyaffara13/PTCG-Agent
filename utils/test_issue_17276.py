
def test_issue_17276():
    assert nonlinsolve([Eq(x, 5**(S(1)/5)), Eq(x*y, 25*sqrt(5))], x, y) == \
     FiniteSet((5**(S(1)/5), 25*5**(S(3)/10)))

