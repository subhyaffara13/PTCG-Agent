
def test_issue_6100_12942_4473():
    assert x**1.0 != x
    assert x != x**1.0
    assert True != x**1.0
    assert x**1.0 is not True
    assert x is not True
    assert x*y != (x*y)**1.0
    # Pow != Symbol
    assert (x**1.0)**1.0 != x
    assert (x**1.0)**2.0 != x**2
    b = Expr()
    assert Pow(b, 1.0, evaluate=False) != b
    # if the following gets distributed as a Mul (x**1.0*y**1.0 then
    # __eq__ methods could be added to Symbol and Pow to detect the
    # power-of-1.0 case.
    assert ((x*y)**1.0).func is Pow

