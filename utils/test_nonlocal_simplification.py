
def test_nonlocal_simplification():
    assert constantsimp(C1 + C2+x*C2, [C1, C2]) == C1 + C2*x

