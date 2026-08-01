
def test_schreier_sims_random():
    assert sorted(Tetra.pgroup.base) == [0, 1]

    S = SymmetricGroup(3)
    base = [0, 1]
    strong_gens = [Permutation([1, 2, 0]), Permutation([1, 0, 2]),
                  Permutation([0, 2, 1])]
    assert S.schreier_sims_random(base, strong_gens, 5) == (base, strong_gens)
    D = DihedralGroup(3)
    _random_prec = {'g': [Permutation([2, 0, 1]), Permutation([1, 2, 0]),
                         Permutation([1, 0, 2])]}
    base = [0, 1]
    strong_gens = [Permutation([1, 2, 0]), Permutation([2, 1, 0]),
                  Permutation([0, 2, 1])]
    assert D.schreier_sims_random([], D.generators, 2,
           _random_prec=_random_prec) == (base, strong_gens)

