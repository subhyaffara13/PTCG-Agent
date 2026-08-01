
def test_constant_mul():
    # We want C1 (Constant) below to absorb the y's, but not the x's
    assert constant_renumber(constantsimp(y*C1, [C1])) == C1*y
    assert constant_renumber(constantsimp(C1*y, [C1])) == C1*y
    assert constant_renumber(constantsimp(x*C1, [C1])) == x*C1
    assert constant_renumber(constantsimp(C1*x, [C1])) == x*C1
    assert constant_renumber(constantsimp(2*C1, [C1])) == C1
    assert constant_renumber(constantsimp(C1*2, [C1])) == C1
    assert constant_renumber(constantsimp(y*C1*x, [C1, y])) == C1*x
    assert constant_renumber(constantsimp(x*y*C1, [C1, y])) == x*C1
    assert constant_renumber(constantsimp(y*x*C1, [C1, y])) == x*C1
    assert constant_renumber(constantsimp(C1*x*y, [C1, y])) == C1*x
    assert constant_renumber(constantsimp(x*C1*y, [C1, y])) == x*C1
    assert constant_renumber(constantsimp(C1*y*(y + 1), [C1])) == C1*y*(y+1)
    assert constant_renumber(constantsimp(y*C1*(y + 1), [C1])) == C1*y*(y+1)
    assert constant_renumber(constantsimp(x*(y*C1), [C1])) == x*y*C1
    assert constant_renumber(constantsimp(x*(C1*y), [C1])) == x*y*C1
    assert constant_renumber(constantsimp(C1*(x*y), [C1, y])) == C1*x
    assert constant_renumber(constantsimp((x*y)*C1, [C1, y])) == x*C1
    assert constant_renumber(constantsimp((y*x)*C1, [C1, y])) == x*C1
    assert constant_renumber(constantsimp(y*(y + 1)*C1, [C1, y])) == C1
    assert constant_renumber(constantsimp((C1*x)*y, [C1, y])) == C1*x
    assert constant_renumber(constantsimp(y*(x*C1), [C1, y])) == x*C1
    assert constant_renumber(constantsimp((x*C1)*y, [C1, y])) == x*C1
    assert constant_renumber(constantsimp(C1*x*y*x*y*2, [C1, y])) == C1*x**2
    assert constant_renumber(constantsimp(C1*x*y*z, [C1, y, z])) == C1*x
    assert constant_renumber(constantsimp(C1*x*y**2*sin(z), [C1, y, z])) == C1*x
    assert constant_renumber(constantsimp(C1*C1, [C1])) == C1
    assert constant_renumber(constantsimp(C1*C2, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C2*C2, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C1*C1*C2, [C1, C2])) == C1
    assert constant_renumber(constantsimp(C1*x*2**x, [C1])) == C1*x*2**x

