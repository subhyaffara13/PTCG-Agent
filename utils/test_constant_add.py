
def test_constant_add():
    assert constant_renumber(constantsimp(C1 + C1, [C1])) == C1
    assert constant_renumber(constantsimp(C1 + 2, [C1])) == C1
    assert constant_renumber(constantsimp(2 + C1, [C1])) == C1
    assert constant_renumber(constantsimp(C1 + y, [C1, y])) == C1
    assert constant_renumber(constantsimp(C1 + x, [C1])) == C1 + x
    assert constant_renumber(constantsimp(C1 + C1, [C1])) == C1
    assert constant_renumber(constantsimp(C1 + C2, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C2 + C1, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C1 + C2 + C1, [C1, C2])) == C1

