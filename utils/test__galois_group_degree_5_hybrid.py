
def test__galois_group_degree_5_hybrid():
    for T, G, alt in test_polys_by_deg[5]:
        assert _galois_group_degree_5_hybrid(Poly(T)) == (G, alt)

