
def test_PolyElement_sqf_list():
    _, x = ring("x", ZZ)

    f = x**5 - x**3 - x**2 + 1
    g = x**3 + 2*x**2 + 2*x + 1
    h = x - 1
    p = x**4 + x**3 - x - 1

    assert f.sqf_part() == p
    assert f.sqf_list() == (1, [(g, 1), (h, 2)])

