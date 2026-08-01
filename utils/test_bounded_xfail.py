
def test_bounded_xfail():
    """We need to support relations in ask for this to work"""
    assert ask(Q.finite(sin(x)**x)) is True
    assert ask(Q.finite(cos(x)**x)) is True

