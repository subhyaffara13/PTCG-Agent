
def test_invert_numbers():
    assert S(2).invert(5) == 3
    assert S(2).invert(Rational(5, 2)) == S.Half
    assert S(2).invert(5.) == S.Half
    assert S(2).invert(S(5)) == 3
    assert S(2.).invert(5) == 0.5
    assert S(sqrt(2)).invert(5) == 1/sqrt(2)
    assert S(sqrt(2)).invert(sqrt(3)) == 1/sqrt(2)

