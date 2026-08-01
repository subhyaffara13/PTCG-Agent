
def test_schreier_sims_incremental():
    identity = Permutation([0, 1, 2, 3, 4])
    TrivialGroup = PermutationGroup([identity])
    base, strong_gens = TrivialGroup.schreier_sims_incremental(base=[0, 1, 2])
    assert _verify_bsgs(TrivialGroup, base, strong_gens) is True
    S = SymmetricGroup(5)
    base, strong_gens = S.schreier_sims_incremental(base=[0, 1, 2])
    assert _verify_bsgs(S, base, strong_gens) is True
    D = DihedralGroup(2)
    base, strong_gens = D.schreier_sims_incremental(base=[1])
    assert _verify_bsgs(D, base, strong_gens) is True
    A = AlternatingGroup(7)
    gens = A.generators[:]
    gen0 = gens[0]
    gen1 = gens[1]
    gen1 = rmul(gen1, ~gen0)
    gen0 = rmul(gen0, gen1)
    gen1 = rmul(gen0, gen1)
    base, strong_gens = A.schreier_sims_incremental(base=[0, 1], gens=gens)
    assert _verify_bsgs(A, base, strong_gens) is True
    C = CyclicGroup(11)
    gen = C.generators[0]
    base, strong_gens = C.schreier_sims_incremental(gens=[gen**3])
    assert _verify_bsgs(C, base, strong_gens) is True

