
def test_issue_7246():
    assert ask(Q.positive(atan(p)), Q.positive(p)) is True
    assert ask(Q.positive(atan(p)), Q.negative(p)) is False
    assert ask(Q.positive(atan(p)), Q.zero(p)) is False
    assert ask(Q.positive(atan(x))) is None

    assert ask(Q.positive(asin(p)), Q.positive(p)) is None
    assert ask(Q.positive(asin(p)), Q.zero(p)) is None
    assert ask(Q.positive(asin(Rational(1, 7)))) is True
    assert ask(Q.positive(asin(x)), Q.positive(x) & Q.nonpositive(x - 1)) is True
    assert ask(Q.positive(asin(x)), Q.negative(x) & Q.nonnegative(x + 1)) is False

    assert ask(Q.positive(acos(p)), Q.positive(p)) is None
    assert ask(Q.positive(acos(Rational(1, 7)))) is True
    assert ask(Q.positive(acos(x)), Q.nonnegative(x + 1) & Q.nonpositive(x - 1)) is True
    assert ask(Q.positive(acos(x)), Q.nonnegative(x - 1)) is None

    assert ask(Q.positive(acot(x)), Q.positive(x)) is True
    assert ask(Q.positive(acot(x)), Q.real(x)) is True
    assert ask(Q.positive(acot(x)), Q.imaginary(x)) is False
    assert ask(Q.positive(acot(x))) is None

