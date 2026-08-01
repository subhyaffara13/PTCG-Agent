
def test_tautology():
    assert ask(Q.real(x) | ~Q.real(x)) is True
    assert ask(Q.real(x) & ~Q.real(x)) is False

