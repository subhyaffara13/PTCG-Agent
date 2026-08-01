
def test_extended_real():
    assert ask(Q.extended_real(x), Q.positive_infinite(x)) is True
    assert ask(Q.extended_real(x), Q.positive(x)) is True
    assert ask(Q.extended_real(x), Q.zero(x)) is True
    assert ask(Q.extended_real(x), Q.negative(x)) is True
    assert ask(Q.extended_real(x), Q.negative_infinite(x)) is True

    assert ask(Q.extended_real(-x), Q.positive(x)) is True
    assert ask(Q.extended_real(-x), Q.negative(x)) is True

    assert ask(Q.extended_real(x + S.Infinity), Q.real(x)) is True

    assert ask(Q.extended_real(x), Q.infinite(x)) is None

