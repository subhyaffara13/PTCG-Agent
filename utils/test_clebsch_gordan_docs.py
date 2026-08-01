
def test_clebsch_gordan_docs():
    assert clebsch_gordan(Rational(3, 2), S.Half, 2, Rational(3, 2), S.Half, 2) == 1
    assert clebsch_gordan(Rational(3, 2), S.Half, 1, Rational(3, 2), Rational(-1, 2), 1) == sqrt(3)/2
    assert clebsch_gordan(Rational(3, 2), S.Half, 1, Rational(-1, 2), S.Half, 0) == -sqrt(2)/2

