
def test_invertible_fullrank():
    assert ask(Q.invertible(X), Q.fullrank(X)) is True

