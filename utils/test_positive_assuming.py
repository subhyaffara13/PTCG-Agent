
def test_positive_assuming():
    with assuming(Q.positive(x + 1)):
        assert not ask(Q.positive(x))

