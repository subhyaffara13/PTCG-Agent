
def test_galois_group_not_by_name():
    """
    Check at least one polynomial of each supported degree, to see that
    conversion from name to group works.
    """
    for deg in range(1, 7):
        T, G_name, _ = test_polys_by_deg[deg][0]
        G, _ = galois_group(T)
        assert G == G_name.get_perm_group()

