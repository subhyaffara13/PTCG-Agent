
def test_non_atoms():
    assert ask(Q.real(Trace(X)), Q.positive(Trace(X)))

