
def test_fateman_poly_F_1():
    f, g, h = fateman_poly_F_1(1)
    F, G, H = dmp_fateman_poly_F_1(1, ZZ)

    assert [ t.rep.to_list() for t in [f, g, h] ] == [F, G, H]

    f, g, h = fateman_poly_F_1(3)
    F, G, H = dmp_fateman_poly_F_1(3, ZZ)

    assert [ t.rep.to_list() for t in [f, g, h] ] == [F, G, H]

