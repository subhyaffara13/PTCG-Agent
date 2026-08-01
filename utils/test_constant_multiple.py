
def test_constant_multiple():
    assert constant_renumber(constantsimp(C1*2 + 2, [C1])) == C1
    assert constant_renumber(constantsimp(x*2/C1, [C1])) == C1*x
    assert constant_renumber(constantsimp(C1**2*2 + 2, [C1])) == C1
    assert constant_renumber(
        constantsimp(sin(2*C1) + x + sqrt(2), [C1])) == C1 + x
    assert constant_renumber(constantsimp(2*C1 + C2, [C1, C2])) == C1

