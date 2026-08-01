
def test_galois_group():
    f = Poly(x ** 4 - 2)
    G, alt = f.galois_group(by_name=True)
    assert G == S4TransitiveSubgroups.D4
    assert alt is False


def test_galois_group():
    """
    Try all the test polys.
    """
    for deg in range(1, 7):
        polys = test_polys_by_deg[deg]
        for T, G, alt in polys:
            assert galois_group(T, by_name=True) == (G, alt)

