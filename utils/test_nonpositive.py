
def test_nonpositive():
    assert ask(Q.nonpositive(-1))
    assert ask(Q.nonpositive(0))
    assert ask(Q.nonpositive(1)) is False
    assert ask(~Q.positive(x), Q.nonpositive(x))
    assert ask(Q.nonpositive(x), Q.positive(x)) is False
    assert ask(Q.nonpositive(sqrt(-1))) is False
    assert ask(Q.nonpositive(x), Q.imaginary(x)) is False

