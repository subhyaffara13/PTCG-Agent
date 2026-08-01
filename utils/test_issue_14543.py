
def test_issue_14543():
    assert sec(2*pi + 11) == sec(11)
    assert sec(2*pi - 11) == sec(11)
    assert sec(pi + 11) == -sec(11)
    assert sec(pi - 11) == -sec(11)

    assert csc(2*pi + 17) == csc(17)
    assert csc(2*pi - 17) == -csc(17)
    assert csc(pi + 17) == -csc(17)
    assert csc(pi - 17) == csc(17)

    x = Symbol('x')
    assert csc(pi/2 + x) == sec(x)
    assert csc(pi/2 - x) == sec(x)
    assert csc(pi*Rational(3, 2) + x) == -sec(x)
    assert csc(pi*Rational(3, 2) - x) == -sec(x)

    assert sec(pi/2 - x) == csc(x)
    assert sec(pi/2 + x) == -csc(x)
    assert sec(pi*Rational(3, 2) + x) == csc(x)
    assert sec(pi*Rational(3, 2) - x) == -csc(x)

