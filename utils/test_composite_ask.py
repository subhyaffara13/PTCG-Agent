
def test_composite_ask():
    assert ask(Q.negative(x) & Q.integer(x),
        assumptions=Q.real(x) >> Q.positive(x)) is False

