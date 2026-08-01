
def test_equality_failing():
    # Note that implementing the substitution property of equality
    # most likely requires a redesign of the new assumptions.
    # See issue #25485 for why this is the case and general ideas
    # about how things could be redesigned.

    # test substitution property
    assert ask(Q.prime(x), Q.eq(x, y) & Q.prime(y)) is True
    assert ask(Q.real(x), Q.eq(x, y) & Q.real(y)) is True
    assert ask(Q.imaginary(x), Q.eq(x, y) & Q.imaginary(y)) is True

