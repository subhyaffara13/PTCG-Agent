
def test_issue_25221():
    assert ask(Q.transcendental(x), Q.algebraic(x) | Q.positive(y,y)) is None
    assert ask(Q.transcendental(x), Q.algebraic(x) | (0 > y)) is None
    assert ask(Q.transcendental(x), Q.algebraic(x) | Q.gt(0,y)) is None

