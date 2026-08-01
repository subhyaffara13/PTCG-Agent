
def test_autosimp_used_to_fail():
    # See issue #9807
    assert ask(Q.imaginary(0**I)) is None
    assert ask(Q.imaginary(0**(-I))) is None
    assert ask(Q.real(0**I)) is None
    assert ask(Q.real(0**(-I))) is None

