
def test_constant_function():
    assert constant_renumber(constantsimp(sin(C1), [C1])) == C1
    assert constant_renumber(constantsimp(f(C1), [C1])) == C1
    assert constant_renumber(constantsimp(f(C1, C1), [C1])) == C1
    assert constant_renumber(constantsimp(f(C1, C2), [C1, C2])) == C1
    assert constant_renumber(constantsimp(f(C2, C1), [C1, C2])) == C1
    assert constant_renumber(constantsimp(f(C2, C2), [C1, C2])) == C1
    assert constant_renumber(
        constantsimp(f(C1, x), [C1])) == f(C1, x)
    assert constant_renumber(constantsimp(f(C1, y), [C1, y])) == C1
    assert constant_renumber(constantsimp(f(y, C1), [C1, y])) == C1
    assert constant_renumber(constantsimp(f(C1, y, C2), [C1, C2, y])) == C1

