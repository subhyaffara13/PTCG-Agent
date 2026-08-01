
def test_constantsimp_take_problem():
    c = exp(C1) + 2
    assert len(Poly(constantsimp(exp(C1) + c + c*x, [C1])).gens) == 2

