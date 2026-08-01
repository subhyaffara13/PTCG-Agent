
def test__galois_group_degree_4_root_approx():
    for T, G, alt in test_polys_by_deg[4]:
        assert _galois_group_degree_4_root_approx(Poly(T)) == (G, alt)

