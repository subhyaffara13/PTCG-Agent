
def test_rubik():
    skip('takes too much time')
    G = PermutationGroup(rubik_cube_generators())
    assert G.order() == 43252003274489856000
    G1 = PermutationGroup(G[:3])
    assert G1.order() == 170659735142400
    assert not G1.is_normal(G)
    G2 = G.normal_closure(G1.generators)
    assert G2.is_subgroup(G)

