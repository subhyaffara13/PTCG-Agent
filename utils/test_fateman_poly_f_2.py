
def test_fateman_poly_F_2():
    f, g, h = fateman_poly_F_2(1)
    F, G, H = dmp_fateman_poly_F_2(1, ZZ)

    assert [ t.rep.to_list() for t in [f, g, h] ] == [F, G, H]

    f, g, h = fateman_poly_F_2(3)
    F, G, H = dmp_fateman_poly_F_2(3, ZZ)

    assert [ t.rep.to_list() for t in [f, g, h] ] == [F, G, H]

