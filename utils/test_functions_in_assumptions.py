
def test_functions_in_assumptions():
    assert ask(Q.negative(x), Q.real(x) >> Q.positive(x)) is False
    assert ask(Q.negative(x), Equivalent(Q.real(x), Q.positive(x))) is False
    assert ask(Q.negative(x), Xor(Q.real(x), Q.negative(x))) is False

