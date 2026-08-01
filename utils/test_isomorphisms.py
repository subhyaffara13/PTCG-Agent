
def test_isomorphisms():

    F, a, b = free_group("a, b")
    E, c, d = free_group("c, d")
    # Infinite groups with differently ordered relators.
    G = FpGroup(F, [a**2, b**3])
    H = FpGroup(F, [b**3, a**2])
    assert is_isomorphic(G, H)

    # Trivial Case
    # FpGroup -> FpGroup
    H = FpGroup(F, [a**3, b**3, (a*b)**2])
    F, c, d = free_group("c, d")
    G = FpGroup(F, [c**3, d**3, (c*d)**2])
    check, T =  group_isomorphism(G, H)
    assert check
    assert T(c**3*d**2) == a**3*b**2

    # FpGroup -> PermutationGroup
    # FpGroup is converted to the equivalent isomorphic group.
    F, a, b = free_group("a, b")
    G = FpGroup(F, [a**3, b**3, (a*b)**2])
    H = AlternatingGroup(4)
    check, T = group_isomorphism(G, H)
    assert check
    assert T(b*a*b**-1*a**-1*b**-1) == Permutation(0, 2, 3)
    assert T(b*a*b*a**-1*b**-1) == Permutation(0, 3, 2)

    # PermutationGroup -> PermutationGroup
    D = DihedralGroup(8)
    p = Permutation(0, 1, 2, 3, 4, 5, 6, 7)
    P = PermutationGroup(p)
    assert not is_isomorphic(D, P)

    A = CyclicGroup(5)
    B = CyclicGroup(7)
    assert not is_isomorphic(A, B)

    # Two groups of the same prime order are isomorphic to each other.
    G = FpGroup(F, [a, b**5])
    H = CyclicGroup(5)
    assert G.order() == H.order()
    assert is_isomorphic(G, H)

