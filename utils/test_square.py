
def test_square():
    assert ask(Q.square(X))
    assert not ask(Q.square(Y))
    assert ask(Q.square(Y*Y.T))

