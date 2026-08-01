
def test_simplify_presentation():
    # ref #16083
    G = simplify_presentation(FpGroup(FreeGroup([]), []))
    assert not G.generators
    assert not G.relators

    # CyclicGroup(3)
    # The second generator in <x, y | x^2, x^5, y^3> is trivial due to relators {x^2, x^5}
    F, x, y = free_group("x, y")
    G = simplify_presentation(FpGroup(F, [x**2, x**5, y**3]))
    assert x in G.relators

