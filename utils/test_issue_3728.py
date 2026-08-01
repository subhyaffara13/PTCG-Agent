
def test_issue_3728():
    assert (Rational(1, 2)*array([2*x, 0]) == array([x, 0])).all()
    assert (Rational(1, 2) + array(
        [2*x, 0]) == array([2*x + Rational(1, 2), Rational(1, 2)])).all()
    assert (Float("0.5")*array([2*x, 0]) == array([Float("1.0")*x, 0])).all()
    assert (Float("0.5") + array(
        [2*x, 0]) == array([2*x + Float("0.5"), Float("0.5")])).all()

