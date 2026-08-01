
def test_constant_power_as_exp():
    assert constant_renumber(constantsimp(x**C1, [C1])) == x**C1
    assert constant_renumber(constantsimp(y**C1, [C1, y])) == C1
    assert constant_renumber(constantsimp(x**y**C1, [C1, y])) == x**C1
    assert constant_renumber(
        constantsimp((x**y)**C1, [C1])) == (x**y)**C1
    assert constant_renumber(
        constantsimp(x**(y**C1), [C1, y])) == x**C1
    assert constant_renumber(constantsimp(x**C1**y, [C1, y])) == x**C1
    assert constant_renumber(
        constantsimp(x**(C1**y), [C1, y])) == x**C1
    assert constant_renumber(
        constantsimp((x**C1)**y, [C1])) == (x**C1)**y
    assert constant_renumber(constantsimp(2**C1, [C1])) == C1
    assert constant_renumber(constantsimp(S(2)**C1, [C1])) == C1
    assert constant_renumber(constantsimp(exp(C1), [C1])) == C1
    assert constant_renumber(
        constantsimp(exp(C1 + x), [C1])) == C1*exp(x)
    assert constant_renumber(constantsimp(Pow(2, C1), [C1])) == C1

