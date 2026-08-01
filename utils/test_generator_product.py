
def test_generator_product():
    G = SymmetricGroup(5)
    p = Permutation(0, 2, 3)(1, 4)
    gens = G.generator_product(p)
    assert all(g in G.strong_gens for g in gens)
    w = G.identity
    for g in gens:
        w = g*w
    assert w == p

