
def test_constant_power_as_base():
    assert constant_renumber(constantsimp(C1**C1, [C1])) == C1
    assert constant_renumber(constantsimp(Pow(C1, C1), [C1])) == C1
    assert constant_renumber(constantsimp(C1**C1, [C1])) == C1
    assert constant_renumber(constantsimp(C1**C2, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C2**C1, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C2**C2, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C1**y, [C1, y])) == C1
    assert constant_renumber(constantsimp(C1**x, [C1])) == C1**x
    assert constant_renumber(constantsimp(C1**2, [C1])) == C1
    assert constant_renumber(
        constantsimp(C1**(x*y), [C1])) == C1**(x*y)

