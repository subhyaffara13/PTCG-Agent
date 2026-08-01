
def test_to_number_field():
    assert to_number_field(sqrt(2)) == AlgebraicNumber(sqrt(2))
    assert to_number_field(
        [sqrt(2), sqrt(3)]) == AlgebraicNumber(sqrt(2) + sqrt(3))

    a = AlgebraicNumber(sqrt(2) + sqrt(3), [S.Half, S.Zero, Rational(-9, 2), S.Zero])

    assert to_number_field(sqrt(2), sqrt(2) + sqrt(3)) == a
    assert to_number_field(sqrt(2), AlgebraicNumber(sqrt(2) + sqrt(3))) == a

    raises(IsomorphismFailed, lambda: to_number_field(sqrt(2), sqrt(3)))

