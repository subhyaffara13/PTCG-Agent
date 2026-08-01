
def test_rubik1():
    gens = rubik_cube_generators()
    gens1 = [gens[-1]] + [p**2 for p in gens[1:]]
    G1 = PermutationGroup(gens1)
    assert G1.order() == 19508428800
    gens2 = [p**2 for p in gens]
    G2 = PermutationGroup(gens2)
    assert G2.order() == 663552
    assert G2.is_subgroup(G1, 0)
    C1 = G1.derived_subgroup()
    assert C1.order() == 4877107200
    assert C1.is_subgroup(G1, 0)
    assert not G2.is_subgroup(C1, 0)

    G = RubikGroup(2)
    assert G.order() == 3674160

