
def test_nonnegative():
    assert ask(Q.nonnegative(-1)) is False
    assert ask(Q.nonnegative(0))
    assert ask(Q.nonnegative(1))
    assert ask(~Q.negative(x), Q.nonnegative(x))
    assert ask(Q.nonnegative(x), Q.negative(x)) is False
    assert ask(Q.nonnegative(sqrt(-1))) is False
    assert ask(Q.nonnegative(x), Q.imaginary(x)) is False

