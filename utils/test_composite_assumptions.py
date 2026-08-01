
def test_composite_assumptions():
    assert ask(Q.real(x), Q.real(x) & Q.real(y)) is True
    assert ask(Q.positive(x), Q.positive(x) | Q.positive(y)) is None
    assert ask(Q.positive(x), Q.real(x) >> Q.positive(y)) is None
    assert ask(Q.real(x), ~(Q.real(x) >> Q.real(y))) is True

