
def test_log_base():
    assert log(1, 2) == 0
    assert log(2, 2) == 1
    assert log(3, 2) == log(3)/log(2)
    assert log(6, 2) == 1 + log(3)/log(2)
    assert log(6, 3) == 1 + log(2)/log(3)
    assert log(2**3, 2) == 3
    assert log(3**3, 3) == 3
    assert log(5, 1) is zoo
    assert log(1, 1) is nan
    assert log(Rational(2, 3), 10) == log(Rational(2, 3))/log(10)
    assert log(Rational(2, 3), Rational(1, 3)) == -log(2)/log(3) + 1
    assert log(Rational(2, 3), Rational(2, 5)) == \
        log(Rational(2, 3))/log(Rational(2, 5))
    # issue 17148
    assert log(Rational(8, 3), 2) == -log(3)/log(2) + 3

