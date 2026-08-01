
def test_baseswap():
    S = SymmetricGroup(4)
    S.schreier_sims()
    base = S.base
    strong_gens = S.strong_gens
    assert base == [0, 1, 2]
    deterministic = S.baseswap(base, strong_gens, 1, randomized=False)
    randomized = S.baseswap(base, strong_gens, 1)
    assert deterministic[0] == [0, 2, 1]
    assert _verify_bsgs(S, deterministic[0], deterministic[1]) is True
    assert randomized[0] == [0, 2, 1]
    assert _verify_bsgs(S, randomized[0], randomized[1]) is True

