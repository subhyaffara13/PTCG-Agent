
def test_isolate():
    assert isolate(1) == (1, 1)
    assert isolate(S.Half) == (S.Half, S.Half)

    assert isolate(sqrt(2)) == (1, 2)
    assert isolate(-sqrt(2)) == (-2, -1)

    assert isolate(sqrt(2), eps=Rational(1, 100)) == (Rational(24, 17), Rational(17, 12))
    assert isolate(-sqrt(2), eps=Rational(1, 100)) == (Rational(-17, 12), Rational(-24, 17))

    raises(NotImplementedError, lambda: isolate(I))

