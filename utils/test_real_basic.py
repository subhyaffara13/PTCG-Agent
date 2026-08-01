
def test_real_basic():
    assert ask(Q.real(x)) is None
    assert ask(Q.real(x), Q.real(x)) is True
    assert ask(Q.real(x), Q.nonzero(x)) is True
    assert ask(Q.real(x), Q.positive(x)) is True
    assert ask(Q.real(x), Q.negative(x)) is True
    assert ask(Q.real(x), Q.integer(x)) is True
    assert ask(Q.real(x), Q.even(x)) is True
    assert ask(Q.real(x), Q.prime(x)) is True

    assert ask(Q.real(x/sqrt(2)), Q.real(x)) is True
    assert ask(Q.real(x/sqrt(-2)), Q.real(x)) is False

    assert ask(Q.real(x + 1), Q.real(x)) is True
    assert ask(Q.real(x + I), Q.real(x)) is False
    assert ask(Q.real(x + I), Q.complex(x)) is None

    assert ask(Q.real(2*x), Q.real(x)) is True
    assert ask(Q.real(I*x), Q.real(x)) is False
    assert ask(Q.real(I*x), Q.imaginary(x)) is True
    assert ask(Q.real(I*x), Q.complex(x)) is None

