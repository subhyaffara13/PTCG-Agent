
def test_core_numbers():
    for c in (Integer(2), Rational(2, 3), Float("1.2")):
        check(c)
    for c in (AlgebraicNumber, AlgebraicNumber(sqrt(3))):
        check(c, check_attr=False)

