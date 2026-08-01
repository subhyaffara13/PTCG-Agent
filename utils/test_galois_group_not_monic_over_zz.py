
def test_galois_group_not_monic_over_ZZ():
    """
    Check that we can work with polys that are not monic over ZZ.
    """
    for deg in range(1, 7):
        T, G, alt = test_polys_by_deg[deg][0]
        assert galois_group(T/2, by_name=True) == (G, alt)

