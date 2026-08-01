
def test_composite_proposition():
    assert ask(True) is True
    assert ask(False) is False
    assert ask(~Q.negative(x), Q.positive(x)) is True
    assert ask(~Q.real(x), Q.commutative(x)) is None
    assert ask(Q.negative(x) & Q.integer(x), Q.positive(x)) is False
    assert ask(Q.negative(x) & Q.integer(x)) is None
    assert ask(Q.real(x) | Q.integer(x), Q.positive(x)) is True
    assert ask(Q.real(x) | Q.integer(x)) is None
    assert ask(Q.real(x) >> Q.positive(x), Q.negative(x)) is False
    assert ask(Implies(
        Q.real(x), Q.positive(x), evaluate=False), Q.negative(x)) is False
    assert ask(Implies(Q.real(x), Q.positive(x), evaluate=False)) is None
    assert ask(Equivalent(Q.integer(x), Q.even(x)), Q.even(x)) is True
    assert ask(Equivalent(Q.integer(x), Q.even(x))) is None
    assert ask(Equivalent(Q.positive(x), Q.integer(x)), Q.integer(x)) is None
    assert ask(Q.real(x) | Q.integer(x), Q.real(x) | Q.integer(x)) is True

