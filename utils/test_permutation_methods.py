
def test_permutation_methods():
    F, x, y = free_group("x, y")
    # DihedralGroup(8)
    G = FpGroup(F, [x**2, y**8, x*y*x**-1*y])
    T = G._to_perm_group()[1]
    assert T.is_isomorphism()
    assert G.center() == [y**4]

    # DiheadralGroup(4)
    G = FpGroup(F, [x**2, y**4, x*y*x**-1*y])
    S = FpSubgroup(G, G.normal_closure([x]))
    assert x in S
    assert y**-1*x*y in S

    # Z_5xZ_4
    G = FpGroup(F, [x*y*x**-1*y**-1, y**5, x**4])
    assert G.is_abelian
    assert G.is_solvable

    # AlternatingGroup(5)
    G = FpGroup(F, [x**3, y**2, (x*y)**5])
    assert not G.is_solvable

    # AlternatingGroup(4)
    G = FpGroup(F, [x**3, y**2, (x*y)**3])
    assert len(G.derived_series()) == 3
    S = FpSubgroup(G, G.derived_subgroup())
    assert S.order() == 4

